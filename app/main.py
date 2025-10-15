from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from app.github_utils import create_repo_and_push
from app.llm_utils import generate_app_code

app = FastAPI()

# --- Root route ---
@app.get("/")
def read_root():
    return {"status": "ok", "message": "LLM Code Deployment API running."}

# --- Request model ---
class TaskRequest(BaseModel):
    email: str
    secret: str
    task: str
    round: int
    nonce: str
    brief: str
    checks: list
    evaluation_url: str
    attachments: list = []

EXPECTED_SECRET = os.getenv("SHARED_SECRET", "my-secret")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in .env")

# --- API endpoint ---
@app.post("/api-endpoint")
async def handle_task(request: TaskRequest):
    # Secret verification
    if request.secret != EXPECTED_SECRET:
        return {"status": "error", "message": "Invalid secret"}

    print(f"✅ Received task: {request.task}, round: {request.round}")

    # Generate app code
    folder = generate_app_code(request.brief, request.task)

    # Create GitHub repo and push files
    try:
        repo_url, commit_sha, pages_url = create_repo_and_push(
            GITHUB_TOKEN, f"{request.task}", folder
        )
    except Exception as e:
        return {"status": "error", "message": f"GitHub push failed: {e}"}

    # Notify evaluation URL
    payload = {
        "email": request.email,
        "task": request.task,
        "round": request.round,
        "nonce": request.nonce,
        "repo_url": repo_url,
        "commit_sha": commit_sha,
        "pages_url": pages_url
    }
    try:
        res = requests.post(request.evaluation_url, json=payload, timeout=10)
        print("📤 Evaluation ping sent:", res.status_code)
    except Exception as e:
        print("⚠️ Failed to contact evaluation URL:", e)

    return {"status": "ok", "repo_url": repo_url, "pages_url": pages_url}

# --- Mock evaluation route ---
@app.post("/eval-mock")
async def eval_mock():
    return {"status": "ok", "message": "Evaluation received"}
