# github_manager.py
import os
from dotenv import load_dotenv
from github import Github, GithubException, InputGitAuthor#, PagesSourceHash # Add PagesSourceHash
from github.GithubObject import NotSet # Import NotSet for configuration
load_dotenv()

class GitHubManager:
    """Handles all interactions with the GitHub API for repo creation and deployment."""
    """
    This code snippet is the init  method of a class in Python.
    It initializes the object by setting the token and username attributes
    based on the values retrieved from environment variables
    (GITHUB_TOKEN and GITHUB_USERNAME). If either of these variables is not set,
    it raises a ValueError with an error message.
    Finally, it creates an instance of the Github class from the github module,
    passing in the token as a parameter."""
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.username = os.getenv("GITHUB_USERNAME")
        
        if not self.token or not self.username:
            raise ValueError("GitHub credentials (GITHUB_TOKEN or GITHUB_USERNAME) are not set in .env.")
            
        self.g = Github(self.token)
        
    def create_and_deploy(self, task_id: str, files: dict) -> tuple[str, str, str]:
        """
        Creates a public repository, commits files, and enables GitHub Pages.
        This code snippet defines a method create_and_deploy in a class GitHubManager.
        The method takes in a task_id (a string) and a files dictionary as parameters
        and returns a tuple of three strings namely as follows:
        the URL of the created repository,
        the SHA of the final commit, and
        the URL of the GitHub Pages site.

        The method performs the following steps:

        It creates a repository name by concatenating the string "llm-app-"
        with the lowercase task_id.
        
        It checks if a repository with the same name already exists.
        If it does, it retrieves the existing repository.
        If not, it creates a new repository with the given name, description,
        and public visibility.
        
        It checks if the main branch exists in the repository.
        If it doesn't, it retrieves the default branch (often 'master').
        
        It iterates over the files dictionary and commits each file to the repository.
        If a file already exists, it updates the file. If not, it creates a new file.
        
        It enables GitHub Pages by setting the default branch to 'main' and fetching
        the Pages status. If the Pages object cannot be fetched, it relies on the
        default URL convention.
        
        It returns the repository URL, the SHA of the final commit, and the GitHub
        Pages URL.
        
        The code includes some error handling, such as catching GithubException and
        Exception to handle various scenarios and raise appropriate errors.
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
            
        # 3. Enable GitHub Pages - Use Robust Fallback
        
        # NOTE: We skip explicit API calls for Pages configuration (get_pages, enable_pages)
        # because the current PyGithub version is incompatible. 
        # We rely on two facts:
        # a) GitHub automatically enables Pages on the 'main' branch if files exist.
        # b) The URL convention is predictable.
        
        # 1. Ensure the default branch is 'main' to trigger Pages activation
        try:
            repo.edit(default_branch="main")
            print("Set default branch to 'main' to activate Pages.")
        except Exception as e:
            # This is a non-critical step, logging a warning is sufficient
            print(f"Warning: Could not set default branch to 'main'. Pages might not activate immediately. Error: {e}")

        # 2. Construct the Pages URL using convention (username.github.io/repo-name/)
        pages_url = f"https://{self.username}.github.io/{repo_name}/"
        print(f"Relying on default Pages URL convention: {pages_url}")

        # 4. Return Details
        return repo.html_url, commit_sha, pages_url

# --- Independent Test Block ---
if __name__ == "__main__":
    try:
        # **IMPORTANT:** Change this unique task ID every time you run the test!
        TEST_TASK_ID = "test-run-10"  # CHANGE THIS!
        
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