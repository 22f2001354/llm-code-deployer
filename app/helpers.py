import os, time, requests
from dotenv import load_dotenv

load_dotenv()
STUDENT_SECRET = os.getenv("STUDENT_SECRET")

def verify_secret(secret):
    return secret == STUDENT_SECRET

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")

def send_evaluation_callback(task_data, repo_info):
    """POST back to evaluation_url with deployment details."""
    payload = {
        "email": task_data["email"],
        "task": task_data["task"],
        "round": task_data["round"],
        "nonce": task_data["nonce"],
        "repo_url": repo_info["repo_url"],
        "commit_sha": repo_info["commit_sha"],
        "pages_url": repo_info["pages_url"],
    }

    delay = 1
    for attempt in range(5):
        try:
            r = requests.post(task_data["evaluation_url"], json=payload)
            if r.status_code == 200:
                log("📤 Evaluation callback successful.")
                return
            else:
                log(f"⚠️ Callback failed ({r.status_code}), retrying...")
        except Exception as e:
            log(f"❌ Callback error: {e}")
        time.sleep(delay)
        delay *= 2
    log("❌ Callback failed after retries.")
