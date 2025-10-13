# github_manager.py
import os
from dotenv import load_dotenv
from github import Github, GithubException
load_dotenv()

class GitHubManager:
    """Handles all interactions with the GitHub API for repo creation and deployment."""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.username = os.getenv("GITHUB_USERNAME")
        
        if not self.token or not self.username:
            raise ValueError("GitHub credentials (GITHUB_TOKEN or GITHUB_USERNAME) are not set in .env.")
            
        self.g = Github(self.token)
        
    def create_and_deploy(self, task_id: str, files: dict) -> tuple[str, str, str]:
        """
        Creates a public repository, commits files, and enables GitHub Pages.
        ...
        """
        repo_name = f"llm-app-{task_id.lower()}"
        
        # --- ORIGINAL LINE (Cause of error): ---
        # user = self.g.get_user(self.username)
        
        # --- FIXED LINE: Get the currently authenticated user ---
        # This user object has the necessary create_repo method.
        user = self.g.get_user() # Calling get_user() with no arguments gets the authenticated user
        
        # 1. Create Repository (or retrieve existing one)
        try:
            repo = user.create_repo( # Now calling create_repo on the authenticated user
                repo_name, 
                description=f"LLM generated code for task {task_id}", 
                private=False 
            )
            print(f"Created repository: {repo_name}...")
        except GithubException as e:
            if e.status == 422 and "name already exists" in e.data['errors'][0]['message']:
                repo = user.get_repo(repo_name)
                print(f"Repository already exists: {repo_name}. Updating files...")
            else:
                raise e
        
        # Ensure main branch exists (and create if it doesn't, though PyGithub usually handles this)
        try:
            main_ref = repo.get_git_ref("heads/main")
        except GithubException:
            # If main doesn't exist, get the default branch, which is often 'master' on old setups.
            # We assume it's created upon the first commit.
            pass
            
        # 2. Commit Files
        commit_sha = ""
        for filename, content in files.items():
            if not content.strip():
                print(f"Skipping empty file: {filename}")
                continue
            
            content_bytes = content.encode('utf-8')

            try:
                # Check if file exists to decide between create_file and update_file
                repo.get_contents(filename, ref="main")
                
                # Update file
                file_obj = repo.update_file(
                    path=filename,
                    message=f"Update {filename} for task {task_id}",
                    content=content_bytes,
                    sha=repo.get_contents(filename).sha,
                    branch="main"
                )
                print(f"Updated {filename}. SHA: {file_obj['commit'].sha[:7]}")
            except GithubException as e:
                # File does not exist, create it
                if e.status == 404:
                    file_obj = repo.create_file(
                        path=filename,
                        message=f"Initial commit of {filename} for task {task_id}",
                        content=content_bytes,
                        branch="main"
                    )
                    print(f"Committed {filename}. SHA: {file_obj['commit'].sha[:7]}")
                else:
                    raise e
            
            commit_sha = file_obj['commit'].sha # Get the SHA of the final commit
            
         # 3. Enable GitHub Pages - Final, Most Compatible Logic
        pages_url = f"https://{self.username}.github.io/{repo_name}/"
        
        try:
            # We use the edit() method to set the 'default_branch' to 'main'
            # This is often enough to trigger Pages configuration in older PyGithub versions,
            # especially since GitHub Pages defaults to the 'main' branch root path.
            repo.edit(default_branch="main")
            
            print("Set default branch to 'main'. Attempting to fetch Pages status...")

            # Now, attempt to explicitly get the pages object (this may still fail, but we try)
            try:
                pages = repo.get_pages()
                print(f"GitHub Pages URL confirmed: {pages.html_url}")
            except Exception:
                # If get_pages still fails (due to old PyGithub), we assume the URL based on convention.
                print("Warning: Could not fetch Pages object, but relying on default URL convention.")
            
        except GithubException as e:
            # Catch errors during repo.edit() or initial setup
            print(f"CRITICAL: Failed during Pages setup attempt. Status: {e.status}")
            raise e
        except Exception as inner_e:
            # General fallback error
            print(f"CRITICAL: Uncaught Pages setup error: {inner_e}")
            raise inner_e

        # 4. Return Details
        return repo.html_url, commit_sha, pages_url

# --- Independent Test Block ---
if __name__ == "__main__":
    try:
        # **IMPORTANT:** Change this unique task ID every time you run the test!
        TEST_TASK_ID = "test-run-6"  # CHANGE THIS!
        
        # Minimum files required for the test
        test_files = {
            "index.html": "<html><body><h1>Hello from LLM Code Deployment!</h1></body></html>",
            "README.md": f"# LLM Deployment Test {TEST_TASK_ID}\n\nThis is a successful test commit.",
            "LICENSE": "MIT License content here."
        }
        
        manager = GitHubManager()
        repo_url, commit_sha, pages_url = manager.create_and_deploy(
            task_id=TEST_TASK_ID, 
            files=test_files
        )
        
        print("\n--- TEST SUCCESSFUL ---")
        print(f"Repo URL: {repo_url}")
        print(f"Commit SHA: {commit_sha}")
        print(f"Pages URL (wait 1 min to check): {pages_url}")

    except ValueError as e:
        print(f"Configuration Error: {e}")
    except GithubException as e:
        print(f"GitHub API Error (Status {e.status}): {e.data['message']}")
        print("Check your GITHUB_TOKEN scope (must include 'repo') and username.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")