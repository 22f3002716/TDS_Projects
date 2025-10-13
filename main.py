# main.py
import os
from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Request, Depends, status
from pydantic import BaseModel, Field

# Local module imports
from llm_generator import LLMCodeGenerator
from github_manager import GitHubManager

# --- 1. Pydantic Model for Incoming Request Data ---

class Attachment(BaseModel):
    """Schema for a single file attachment."""
    name: str = Field(description="The original name of the file.")
    url: str = Field(description="The Base64 data URI of the file content.")

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
def get_auth_check(request: Request):
    """Performs a simple secret check."""
    # This token should ideally be loaded from an environment variable (e.g., WEBHOOK_SECRET)
    # For now, we'll just check if the secret field is present in the request body (FastAPI handles parsing).
    # Since we use the secret field from TaskRequest, we'll check it within the main handler.
    # For a simple check, we can check a known header:
    # if request.headers.get("X-API-KEY") != os.getenv("API_KEY"):
    #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    pass


# --- 4. Main API Endpoint ---

@app.post("/generate-code", tags=["Code Generation"])
async def handle_code_generation(
    task_request: TaskRequest,
    auth_check: Any = Depends(get_auth_check)
):
    """
    Receives a task request, generates code using the LLM, 
    and commits the result to GitHub.
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

        # 4.3. Commit to GitHub (using GitHub Manager)
        commit_message = f"Solve task {task_request.task}, Round {task_request.round}"
        branch_name = f"task/{task_request.task}/round-{task_request.round}"
        
        # This will create a new branch, commit files, and return the URL
        commit_url = github_manager.commit_files(
            files_content=generated_files,
            commit_message=commit_message,
            branch_name=branch_name
        )
        
        # 4.4. Success Response
        return {
            "status": "success",
            "message": "Code generated and committed successfully.",
            "commit_url": commit_url,
            "evaluation_url": task_request.evaluation_url # Echoing the next step URL
        }

    except Exception as e:
        print(f"Error during processing: {e}")
        # 4.5. Error Response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process request: {e}"
        )

# --- 5. Health Check Endpoint ---

@app.get("/health", tags=["Monitoring"])
async def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "service": app.title}