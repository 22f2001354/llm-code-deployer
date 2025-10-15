from github import Github
from dotenv import load_dotenv
import os
import subprocess
import requests

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found in .env")

g = Github(GITHUB_TOKEN)
user = g.get_user()

def create_repo_and_push(token, repo_name, folder_path):
    """
    Create a GitHub repo, push local folder, enable Pages.
    Returns repo URL, commit SHA, and GitHub Pages URL.
    """
    # --- 1. Create repo ---
    repo = user.create_repo(repo_name, private=False, auto_init=False)
    repo_url = repo.clone_url

    # --- 2. Git push ---
    subprocess.run(["git", "init"], cwd=folder_path)
    subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=folder_path)
    subprocess.run(["git", "add", "."], cwd=folder_path)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=folder_path)
    subprocess.run(["git", "branch", "-M", "main"], cwd=folder_path)
    subprocess.run(["git", "push", "-u", "origin", "main"], cwd=folder_path)

    # --- 3. Enable GitHub Pages via API ---
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    pages_api = f"https://api.github.com/repos/{user.login}/{repo_name}/pages"
    data = {"source": {"branch": "main", "path": "/"}}
    res = requests.post(pages_api, headers=headers, json=data)
    if res.status_code in [201, 204]:
        print(f"✅ GitHub Pages enabled at https://{user.login}.github.io/{repo_name}/")
    else:
        print(f"⚠️ Failed to enable GitHub Pages: {res.status_code} {res.text}")

    # --- 4. Return ---
    commit_sha = repo.get_commits()[0].sha
    pages_url = f"https://{user.login}.github.io/{repo_name}/"
    return repo_url, commit_sha, pages_url
