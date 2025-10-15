# LLM Code Deployment

This project automates the process of **building, deploying, and updating** small web applications using LLMs and GitHub Pages.

## 🚀 Workflow
1. Receive JSON request from instructor.
2. Verify student secret.
3. Use LLM to generate minimal app code.
4. Push to GitHub & enable Pages.
5. Notify evaluation URL.
6. On Round 2: Update existing repo and redeploy.

## 🧰 Stack
- FastAPI
- OpenAI GPT
- GitHub API (PyGithub)
- Render / Railway for hosting

## 📤 API Endpoint
POST `/api-endpoint`

## ⚙️ Environment
- `STUDENT_SECRET`
- `GITHUB_TOKEN`
- `OPENAI_API_KEY`
- `GITHUB_USERNAME`
