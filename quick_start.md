# ⚡ Quick Start Guide

Get up and running in 10 minutes!

## 1️⃣ Install UV

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Mac/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 2️⃣ Clone & Setup

```bash
# Create project directory
mkdir llm-code-deployer
cd llm-code-deployer

# Create folder structure
mkdir -p modules database utils prompts tests logs
touch modules/__init__.py database/__init__.py utils/__init__.py prompts/__init__.py tests/__init__.py

# Copy all code files from artifacts into respective folders
# (See SETUP_GUIDE.md for complete file list)
```

## 3️⃣ Get API Keys

1. **GitHub Token:** https://github.com/settings/tokens
   - Scopes: `repo`, `workflow`, `admin:repo_hook`

2. **Gemini API:** https://makersuite.google.com/app/apikey
   - Free tier available

## 4️⃣ Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your keys
# Required fields:
# - STUDENT_SECRET
# - GEMINI_API_KEY
# - GITHUB_TOKEN
# - GITHUB_USERNAME
```

## 5️⃣ Install Dependencies

```bash
# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate  # Mac/Linux
# OR
.venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -e .
```

## 6️⃣ Test & Run

```bash
# Verify configuration
python config.py

# Run tests
pytest tests/ -v

# Start server
python app.py
```

Server will be available at: http://localhost:7860

## 7️⃣ Test Deployment

```bash
# Test health endpoint
curl http://localhost:7860/

# Test deployment (edit with your values)
curl -X POST http://localhost:7860/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "secret": "your-student-secret",
    "task": "test-hello-world",
    "round": 1,
    "nonce": "abc123",
    "brief": "Create a Bootstrap page with Hello World",
    "checks": ["Has h1 tag", "Has Bootstrap"],
    "evaluation_url": "https://httpbin.org/post",
    "attachments": []
  }'
```

## 🎉 Done!

Check your GitHub account for the new repository, and visit the GitHub Pages URL to see your deployed app!

---

## 📚 Next Steps

- Read `SETUP_GUIDE.md` for detailed explanations
- Check `tests/sample_payloads.json` for more examples
- Deploy to Hugging Face Spaces (see SETUP_GUIDE.md Part 8)

## 🐛 Troubleshooting

**Config errors?**
```bash
# Check your .env file
cat .env
```

**Import errors?**
```bash
# Reinstall dependencies
uv pip install -e .
```

**GitHub API errors?**
- Verify token has correct permissions
- Check rate limits: https://github.com/settings/tokens

**LLM errors?**
- Verify API key is valid
- Check quota at: https://makersuite.google.com/