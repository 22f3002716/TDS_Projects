# 🚀 Complete Setup Guide - LLM Code Deployer

This guide will walk you through setting up the entire project from scratch, even if you're a complete beginner.

## 📋 Prerequisites

Before starting, you'll need:

1. **Python 3.10 or higher** - [Download here](https://www.python.org/downloads/)
2. **Visual Studio Code** - [Download here](https://code.visualstudio.com/)
3. **Git** - [Download here](https://git-scm.com/downloads)
4. **GitHub Account** - [Sign up here](https://github.com/join)
5. **Hugging Face Account** - [Sign up here](https://huggingface.co/join)

---

## 🔧 Part 1: Initial Setup (One-Time Configuration)

### Step 1: Install UV Package Manager

UV is a modern, fast Python package manager that makes dependency management simple.

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Verify installation:**
```bash
uv --version
```

### Step 2: Create Project Directory

Open your terminal/command prompt and run:

```bash
# Create project folder
mkdir llm-code-deployer
cd llm-code-deployer

# Initialize Git
git init
```

### Step 3: Create Project Structure

Create the following folder structure:

```
llm-code-deployer/
├── modules/
│   └── __init__.py
├── database/
│   └── __init__.py
├── utils/
│   └── __init__.py
├── prompts/
│   └── __init__.py
├── tests/
│   └── __init__.py
└── logs/
    └── .gitkeep
```

**Quick command to create all folders:**

```bash
mkdir -p modules database utils prompts tests logs
touch modules/__init__.py database/__init__.py utils/__init__.py prompts/__init__.py tests/__init__.py logs/.gitkeep
```

---

## 🔑 Part 2: Get API Keys

### A. GitHub Personal Access Token

1. Go to [GitHub Settings → Developer Settings](https://github.com/settings/tokens)
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: `llm-deployer-token`
4. Select these scopes:
   - ✅ `repo` (all)
   - ✅ `workflow`
   - ✅ `admin:repo_hook`
5. Click **"Generate token"**
6. **⚠️ IMPORTANT:** Copy the token immediately (you won't see it again!)

### B. Gemini API Key (Recommended - Free)

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy your API key

**Alternative: OpenAI API Key**
- Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
- Note: Requires payment setup

---

## 💻 Part 3: VS Code Setup

### Step 1: Open Project in VS Code

```bash
code .
```

### Step 2: Install VS Code Extensions

Install these recommended extensions:
- **Python** (by Microsoft)
- **Pylance** (by Microsoft)
- **Python Debugger** (by Microsoft)

### Step 3: Create Python Files

Copy all the code files I provided earlier into their respective locations:

1. `pyproject.toml` - in root directory
2. `.env.example` - in root directory
3. `.gitignore` - in root directory
4. `config.py` - in root directory
5. `app.py` - in root directory
6. `database/models.py`
7. `utils/logger.py`
8. `utils/validators.py`
9. `prompts/code_generation.py`
10. `prompts/code_revision.py`
11. `modules/llm_integration.py`
12. `modules/github_automation.py`
13. `modules/evaluation_notifier.py`
14. `modules/api_handler.py`
15. `tests/sample_payloads.json`
16. `tests/test_api_handler.py`

---

## 🎯 Part 4: Configure Environment

### Step 1: Create .env File

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### Step 2: Edit .env File

Open `.env` in VS Code and fill in your values:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=my-super-secret-key-12345

# Student Authentication
STUDENT_SECRET=your-secret-that-you-will-share-in-google-form

# LLM API Keys
GEMINI_API_KEY=your-gemini-api-key-here
# OPENAI_API_KEY=your-openai-key-if-using-openai

# Choose LLM Provider
LLM_PROVIDER=gemini

# GitHub Configuration
GITHUB_TOKEN=your-github-personal-access-token-here
GITHUB_USERNAME=your-github-username

# Database
DATABASE_PATH=./database/deployments.db

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Retry Configuration
MAX_RETRY_ATTEMPTS=5
RETRY_DELAYS=1,2,4,8,16
```

**⚠️ NEVER commit the .env file to Git!**

---

## 📦 Part 5: Install Dependencies with UV

### Step 1: Create Virtual Environment

```bash
uv venv
```

This creates a `.venv` folder.

### Step 2: Activate Virtual Environment

**Windows:**
```powershell
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
uv pip install -e .
```

This installs all dependencies from `pyproject.toml`.

### Step 4: Verify Installation

```bash
python -c "import flask; import github; import google.generativeai; print('✅ All imports successful!')"
```

---

## 🧪 Part 6: Test Individual Modules

### Test 1: Configuration

```bash
python config.py
```

**Expected output:**
```
✅ Configuration validated successfully
```

If you see errors, check your `.env` file.

### Test 2: Database

```python
# Create test_database.py
from database.models import Database

db = Database()
print("✅ Database initialized successfully")
print(f"Database location: {db.db_path}")
```

Run it:
```bash
python test_database.py
```

### Test 3: LLM Integration

```python
# Create test_llm.py
from modules.llm_integration import LLMIntegration

llm = LLMIntegration()
print(f"✅ LLM initialized: {llm.provider}")

# Test simple generation
html, readme = llm.generate_application_code(
    brief="Create a simple HTML page that says Hello World",
    checks=["Page has title", "Page has h1 tag"],
    attachments=[]
)

print(f"✅ Generated HTML ({len(html)} chars)")
print(f"✅ Generated README ({len(readme)} chars)")
```

Run it:
```bash
python test_llm.py
```

### Test 4: GitHub Automation

```python
# Create test_github.py
from modules.github_automation import GitHubAutomation

github = GitHubAutomation()
print(f"✅ GitHub authenticated as: {github.user.login}")

# List your repositories
repos = github.user.get_repos()
print(f"✅ You have {repos.totalCount} repositories")
```

Run it:
```bash
python test_github.py
```

### Test 5: Full Integration Test

```bash
python -m pytest tests/test_api_handler.py -v
```

---

## 🚀 Part 7: Run the Application Locally

### Step 1: Start Flask Server

```bash
python app.py
```

**Expected output:**
```
✅ Configuration validated successfully
✅ Database initialized
✅ Gemini client initialized
✅ GitHub authenticated as: your-username
✅ APIHandler initialized
🚀 Starting LLM Code Deployer API...
🤖 LLM Provider: gemini
👤 GitHub User: your-username
 * Running on http://0.0.0.0:7860
```

### Step 2: Test Health Endpoint

Open a new terminal and run:

```bash
curl http://localhost:7860/
```

**Expected response:**
```json
{
  "status": "online",
  "service": "LLM Code Deployer",
  "version": "1.0.0",
  "llm_provider": "gemini"
}
```

### Step 3: Test Deployment Endpoint

```bash
curl -X POST http://localhost:7860/api/deploy \
  -H "Content-Type: application/json" \
  -d @tests/sample_payloads.json
```

Note: You'll need to extract one payload from the JSON file first.

---

## 🌐 Part 8: Deploy to Hugging Face Spaces

### Step 1: Create Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click **"Create new Space"**
3. Fill in:
   - **Space name:** `llm-code-deployer`
   - **License:** MIT
   - **SDK:** Gradio (we'll change this)
   - **Visibility:** Public
4. Click **"Create Space"**

### Step 2: Prepare for Deployment

Create `requirements.txt` (Hugging Face doesn't support pyproject.toml directly):

```bash
uv pip freeze > requirements.txt
```

### Step 3: Create README.md for Hugging Face

```markdown
---
title: LLM Code Deployer
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
---

# LLM Code Deployer

Automated code generation and deployment system using LLMs.
```

### Step 4: Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 7860

# Set environment
ENV PORT=7860

# Run application
CMD ["python", "app.py"]
```

### Step 5: Push to Hugging Face

```bash
# Add Hugging Face remote
git remote add hf https://huggingface.co/spaces/YOUR-USERNAME/llm-code-deployer

# Add all files
git add .
git commit -m "Initial deployment"

# Push to Hugging Face
git push hf main
```

### Step 6: Configure Secrets on Hugging Face

1. Go to your Space settings
2. Click **"Repository secrets"**
3. Add each variable from your `.env` file as a secret

---

## 🎯 Part 9: Testing the Live Deployment

### Test with cURL

```bash
curl -X POST https://YOUR-USERNAME-llm-code-deployer.hf.space/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "secret": "your-secret",
    "task": "test-task-123",
    "round": 1,
    "nonce": "abc123",
    "brief": "Create a Hello World page with Bootstrap",
    "checks": ["Has Bootstrap", "Has h1 tag"],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
  }'
```

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Reinstall dependencies
uv pip install -e .
```

### Issue: "Configuration errors"

**Solution:**
- Check your `.env` file has all required values
- Verify API keys are correct
- Ensure no extra spaces in .env

### Issue: GitHub API rate limit

**Solution:**
- Wait 1 hour for rate limit reset
- Use authenticated requests (make sure GITHUB_TOKEN is set)

### Issue: LLM API errors

**Solution:**
- Verify API key is valid
- Check API quota/billing
- Try a different LLM provider

### Issue: "GitHub Pages not enabled"

**Solution:**
- Manually enable in repo settings: Settings → Pages
- Select Source: Deploy from a branch → main → /

---

## 📊 Part 10: Monitoring and Logs

### View Logs

```bash
tail -f logs/app.log
```

### Check Database

```python
from database.models import Database

db = Database()
conn = db.get_connection()
cursor = conn.cursor()

# View all tasks
cursor.execute("SELECT * FROM tasks")
for row in cursor.fetchall():
    print(dict(row))

# View all deployments
cursor.execute("SELECT * FROM deployments")
for row in cursor.fetchall():
    print(dict(row))

conn.close()
```

---

## 🎓 Part 11: Understanding the Workflow

### Round 1 Flow (Build)

1. **Receive Request** → POST to `/api/deploy`
2. **Validate** → Check email, secret, required fields
3. **Save Task** → Store in database
4. **Generate Code** → LLM creates HTML + README
5. **Create Repo** → Push to GitHub
6. **Enable Pages** → Activate GitHub Pages
7. **Save Deployment** → Store repo info in database
8. **Notify Evaluation** → POST to evaluation_url

### Round 2 Flow (Revise)

1. **Receive Request** → POST to `/api/deploy` with round=2
2. **Validate** → Check email, secret, required fields
3. **Retrieve Round 1** → Fetch existing code from database/GitHub
4. **Generate Updated Code** → LLM modifies existing code
5. **Update Repo** → Push changes to GitHub
6. **Save Deployment** → Store Round 2 info
7. **Notify Evaluation** → POST to evaluation_url

---

## 🔍 Part 12: Advanced Configuration

### Using OpenAI Instead of Gemini

1. Update `.env`:
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

2. Restart application

### Custom Retry Logic

Edit `.env`:
```env
MAX_RETRY_ATTEMPTS=10
RETRY_DELAYS=1,2,4,8,16,32,64
```

### Custom GitHub Pages Path

Modify `modules/github_automation.py`:
```python
response = requests.post(
    f'https://api.github.com/repos/{self.user.login}/{repo.name}/pages',
    headers=headers,
    json={
        'source': {
            'branch': 'main',
            'path': '/docs'  # Changed from '/'
        }
    }
)
```

---

## 📚 Part 13: Code Walkthrough

### Key Files Explained

#### `app.py`
- Entry point for Flask application
- Defines API endpoints
- Handles HTTP requests/responses

#### `config.py`
- Manages environment variables
- Validates configuration
- Provides settings to all modules

#### `modules/api_handler.py`
- Orchestrates the entire workflow
- Routes requests to Round 1 or Round 2
- Coordinates between LLM, GitHub, and database

#### `modules/llm_integration.py`
- Interfaces with LLM APIs
- Generates code from prompts
- Handles code revision

#### `modules/github_automation.py`
- Creates/updates repositories
- Uploads files
- Enables GitHub Pages

#### `modules/evaluation_notifier.py`
- POSTs to evaluation API
- Implements retry logic
- Handles failures gracefully

#### `database/models.py`
- SQLite database operations
- Stores tasks and deployments
- Provides data persistence

---

## 🧪 Part 14: Manual Testing Guide

### Test 1: Simple Hello World (Round 1)

**Payload:**
```json
{
  "email": "your-email@example.com",
  "secret": "your-secret",
  "task": "hello-world-001",
  "round": 1,
  "nonce": "test-001",
  "brief": "Create a Bootstrap 5 page with a centered h1 saying 'Hello World' and a blue button that shows an alert when clicked.",
  "checks": [
    "Page has Bootstrap 5 loaded",
    "h1 element contains 'Hello World'",
    "Button shows alert on click"
  ],
  "evaluation_url": "https://httpbin.org/post",
  "attachments": []
}
```

**Expected Result:**
- New GitHub repo created: `hello-world-001`
- Repo contains: `index.html`, `README.md`, `LICENSE`
- GitHub Pages accessible at: `https://YOUR-USERNAME.github.io/hello-world-001/`
- Page displays "Hello World" with working button

### Test 2: CSV Data Processor (Round 1)

**Payload:**
```json
{
  "email": "your-email@example.com",
  "secret": "your-secret",
  "task": "csv-processor-002",
  "round": 1,
  "nonce": "test-002",
  "brief": "Create a page that parses the attached CSV, calculates the sum of the 'amount' column, and displays it in a div with id='total'.",
  "checks": [
    "CSV data is parsed",
    "Sum is calculated correctly",
    "Result displayed in #total"
  ],
  "evaluation_url": "https://httpbin.org/post",
  "attachments": [
    {
      "name": "data.csv",
      "url": "data:text/csv;base64,aXRlbSxhbW91bnQKQXBwbGUsMTAKQmFuYW5hLDIwCkNoZXJyeSw3MA=="
    }
  ]
}
```

**Expected Result:**
- Repo created with CSV processing code
- Page displays total: 100 (10+20+70)

### Test 3: Add Dark Mode (Round 2)

**Payload:**
```json
{
  "email": "your-email@example.com",
  "secret": "your-secret",
  "task": "hello-world-001",
  "round": 2,
  "nonce": "test-003",
  "brief": "Add a dark mode toggle button. When clicked, switch between light and dark themes. The button should have id='theme-toggle'.",
  "checks": [
    "Button #theme-toggle exists",
    "Clicking toggles dark/light theme",
    "Original functionality still works"
  ],
  "evaluation_url": "https://httpbin.org/post",
  "attachments": []
}
```

**Expected Result:**
- Existing repo `hello-world-001` updated
- New commit with dark mode feature
- Original "Hello World" functionality preserved
- New toggle button working

---

## 📋 Part 15: Common Issues & Solutions

### Issue: "Secret validation failed"

**Cause:** Secret in request doesn't match STUDENT_SECRET in .env

**Solution:**
```bash
# Check your .env file
cat .env | grep STUDENT_SECRET

# Update the secret in your test payload to match
```

### Issue: "GitHub Pages not accessible (404)"

**Cause:** GitHub Pages takes 1-2 minutes to build

**Solution:**
- Wait 2 minutes after deployment
- Check repo Settings → Pages for build status
- Verify `index.html` exists in main branch

### Issue: "LLM generates invalid HTML"

**Cause:** LLM output may include markdown formatting

**Solution:**
- The `extract_code_block()` function should handle this
- If issues persist, check `modules/llm_integration.py`
- Add more specific prompts in `prompts/code_generation.py`

### Issue: "Database locked" error

**Cause:** Multiple simultaneous requests to SQLite

**Solution:**
```python
# In database/models.py, add timeout
conn = sqlite3.connect(self.db_path, timeout=10)
```

### Issue: "Evaluation API timeout"

**Cause:** Evaluation endpoint is slow/unreachable

**Solution:**
- Check `MAX_RETRY_ATTEMPTS` in .env
- Increase timeout in `modules/evaluation_notifier.py`:
```python
response = requests.post(
    evaluation_url,
    json=payload,
    headers={'Content-Type': 'application/json'},
    timeout=60  # Increased from 30
)
```

---

## 🎯 Part 16: Production Deployment Checklist

Before deploying to production:

- [ ] All API keys are set as secrets (not in code)
- [ ] `.env` file is in `.gitignore`
- [ ] Database path is writable
- [ ] Logs directory exists and is writable
- [ ] GitHub token has correct permissions
- [ ] LLM API has sufficient quota
- [ ] Error handling is comprehensive
- [ ] Retry logic is configured
- [ ] STUDENT_SECRET is strong and unique
- [ ] All tests pass: `pytest tests/ -v`

---

## 🚀 Part 17: Next Steps

### Enhancements You Can Add

1. **Add more LLM providers:**
   - Claude (Anthropic)
   - Llama via Together AI
   - Mistral AI

2. **Improve error handling:**
   - Email notifications on failure
   - Slack/Discord webhooks
   - Detailed error logs

3. **Add caching:**
   - Cache LLM responses for similar requests
   - Cache GitHub API calls

4. **Add monitoring:**
   - Prometheus metrics
   - Grafana dashboards
   - Uptime monitoring

5. **Add security:**
   - Rate limiting per email
   - IP whitelisting
   - Request signing/verification

6. **Improve code generation:**
   - Better prompt engineering
   - Multiple LLM calls for refinement
   - Code validation before deployment

---

## 📞 Support & Resources

### Documentation Links

- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Hugging Face Spaces Documentation](https://huggingface.co/docs/hub/spaces)

### Getting Help

If you encounter issues:

1. Check the logs: `tail -f logs/app.log`
2. Verify configuration: `python config.py`
3. Test modules individually (Part 6)
4. Check GitHub repo settings
5. Verify API keys are valid

---

## ✅ Final Verification

Run this checklist to ensure everything works:

```bash
# 1. Virtual environment active?
which python  # Should show .venv path

# 2. Dependencies installed?
python -c "import flask; import github; print('OK')"

# 3. Configuration valid?
python config.py

# 4. Database working?
python -c "from database.models import Database; db = Database(); print('OK')"

# 5. Tests passing?
pytest tests/ -v

# 6. Server starts?
python app.py
```

If all checks pass: **🎉 Congratulations! Your system is ready!**

---

## 📝 Summary

You've now built a complete LLM-powered code deployment system that:

✅ Accepts task requests via API  
✅ Generates code using LLMs  
✅ Creates GitHub repositories  
✅ Deploys to GitHub Pages  
✅ Handles Round 2 revisions  
✅ Notifies evaluation APIs  
✅ Tracks all deployments  

This system is production-ready and can handle the full evaluation workflow described in your project requirements.