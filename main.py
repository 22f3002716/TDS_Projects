# main.py
import os
import httpx # Required for the asynchronous HTTP client
from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Depends, status
from pydantic import BaseModel, Field

# Load environment variables for the secret check
load_dotenv()

# Local module imports
from llm_generator import LLMCodeGenerator
from github_manager import GitHubManager

# --- 1. Pydantic Model for Incoming Request Data ---

class Attachment(BaseModel):
    """Schema for a single file attachment.
    This class definition creates a Pydantic model named Attachment that represents
    a single file attachment. It has two fields: name and url. The name field stores
    the original name of the file, and the url field stores the Base64 data URI of the
    file content. The Field class is used to provide descriptions for the fields."""
    name: str = Field(description="The original name of the file.")
    url: str = Field(description="The Base64 data URI of the file content.")

"""This class definition creates a Pydantic model named TaskRequest that represents
the complete schema for the incoming POST request body. The class has the following
fields:

email: The user's email address.
secret: A secret key for authentication (optional).
task: The unique identifier for the task.
round: The current round/iteration number.
nonce: A unique token for the request.
brief: The detailed task description for the LLM.
checks: A list of verification checks/tests (default is an empty list).
evaluation_url: The URL to notify after completion.
attachments: A list of attached files (default is an empty list).
Each field is annotated with a description using the Field class from Pydantic."""
class TaskRequest(BaseModel):
    """The complete schema for the incoming POST request body."""
    email: str = Field(description="The user's email address.")
    secret: str = Field(description="A secret key for authentication (optional).")
    task: str = Field(description="The unique identifier for the task.")
    round: int = Field(description="The current round/iteration number.")
    nonce: str = Field(description="A unique token for the request.")
    brief: str = Field(description="The detailed task description for the LLM.")
    checks: List[str] = Field(default_factory=list, description="List of verification checks/tests.")
    evaluation_url: str = Field(description="URL to notify after completion.")
    attachments: List[Attachment] = Field(default_factory=list, description="List of attached files.")


# --- 2. Application Setup and Lifespan ---

# Initialize the LLM and GitHub client globally
llm_generator: Optional[LLMCodeGenerator] = None
github_manager: Optional[GitHubManager] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes external resources (LLM and GitHub clients) on startup."""
    global llm_generator, github_manager
    
    # Initialize the LLM (will load the GEMINI_API_KEY)
    try:
        llm_generator = LLMCodeGenerator()
    except ValueError as e:
        print(f"FATAL: LLM initialization failed - {e}")
        # We allow the app to start, but the endpoint will fail

    # Initialize the GitHub Manager (will load the GITHUB_TOKEN)
    try:
        github_manager = GitHubManager()
    except ValueError as e:
        print(f"FATAL: GitHub initialization failed - {e}")
        # We allow the app to start, but the endpoint will fail

    print("FastAPI application startup complete. Modules initialized.")
    yield
    print("FastAPI application shutdown.")

app = FastAPI(
    title="Code Generation Service (Gemini + GitHub)",
    description="A service that generates code using Gemini and commits it to a GitHub repository.",
    version="1.0.0",
    lifespan=lifespan # Attach the lifespan context manager
)

# --- 3. Dependency Function for Authentication ---

# NOTE: This is a placeholder for basic secret authentication.
# In a production environment, this should be replaced by a more robust mechanism (e.g., JWT).
def get_auth_check(task_request: TaskRequest):
    """Performs a simple secret check against the WEBHOOK_SECRET environment variable."""
    expected_secret = os.getenv("WEBHOOK_SECRET")

    # Check if the secret is configured on the server
    if not expected_secret:
        # For testing/dev, we allow access if no secret is set. 
        # In production, this should be a hard failure.
        print("Warning: WEBHOOK_SECRET is not configured on the server.")
        return

    # Check the secret provided in the request body
    if task_request.secret != expected_secret:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid request secret provided."
        )
    # If the secrets match, authentication is successful.


# --- 4. Main API Endpoint ---

@app.post("/generate-code", tags=["Code Generation"])
async def handle_code_generation(
    task_request: TaskRequest,
    # NOTE: Pass TaskRequest to dependency for validation
    auth_check: Any = Depends(get_auth_check) 
):
    """
    Receives a task request, generates code using the LLM, 
    and deploys the result to a NEW GitHub repository.
    """
    global llm_generator, github_manager

    # 4.1. Check for valid service initialization
    if not llm_generator or not github_manager:
          raise HTTPException(
              status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
              detail="Service not fully initialized. Check server logs for missing API keys."
          )

    try:
        # 4.2. Generate Code (using LLM Generator)
        print(f"Processing request for task: {task_request.task}, round: {task_request.round}")
        
        # Convert the Pydantic model to a standard dictionary for the LLM module
        task_data_dict = task_request.model_dump()
        generated_files = llm_generator.generate_app_files(task_data_dict)

        if not generated_files:
            raise ValueError("LLM failed to generate any files.")

        # --- 4.3. CALL FIX: Use create_and_deploy and unpack the three return values ---
        task_slug = task_request.task.lower().replace(" ", "-")
        task_id = f"{task_slug}-round-{task_request.round}"
        
        repo_url, commit_sha, pages_url = github_manager.create_and_deploy(
            task_id=task_id,
            files=generated_files
        )
        # We use the repo_url or pages_url as the final output URL for the user
        final_url = pages_url if pages_url else repo_url
        
        # 4.4. Post to Evaluation URL (Callback)
        try:
            callback_json = {
                "email": task_request.email,
                "task": task_request.task,
                "round": task_request.round,
                "nonce": task_request.nonce,
                "repo_url": repo_url,
                "commit_sha": commit_sha,
                "pages_url": pages_url,
            }
            
            async with httpx.AsyncClient(timeout=600.0) as client: # Timeout is 10 min (600s)
                response = await client.post(
                    task_request.evaluation_url,
                    json=callback_json,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status() # Raise error for 4xx/5xx responses
            
            print(f"Successfully posted results to evaluation URL: {task_request.evaluation_url}")
            
        except httpx.RequestError as e:
            print(f"WARNING: Failed to post to evaluation URL. Request error: {e}")
        except httpx.HTTPStatusError as e:
            print(f"WARNING: Failed to post to evaluation URL. Server returned status: {e.response.status_code}")
        
        # 4.5. Success Response
        return {
            "status": "success",
            "message": f"Code generated and deployed successfully to new repository: {repo_url}",
            "commit_url": final_url, # Return the deployment URL
            "evaluation_url": task_request.evaluation_url
        }

    except Exception as e:
        print(f"Error during processing: {e}")
        # 4.6. Error Response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process request: {e}"
        )
# --- 5. Health Check Endpoint ---

@app.get("/health", tags=["Monitoring"])
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "service": app.title}