# 🚀 LLM Code Deployer

An automated system that uses Large Language Models to generate, deploy, and revise web applications to GitHub Pages.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

This system automates the entire workflow of:
1. **Receiving** task requests via REST API
2. **Generating** application code using LLMs (Gemini/OpenAI/Claude)
3. **Creating** GitHub repositories with generated code
4. **Deploying** to GitHub Pages
5. **Revising** applications based on new requirements
6. **Notifying** evaluation APIs with deployment metadata

Perfect for educational environments, coding assessments, or rapid prototyping.

## ✨ Features

- 🤖 **Multi-LLM Support**: Gemini, OpenAI, or Anthropic Claude
- 🔄 **Two-Round Workflow**: Initial build + revision capability
- 📦 **Automated GitHub Integration**: Repository creation, file uploads, Pages deployment
- 💾 **State Management**: SQLite database tracks all deployments
- 🔁 **Retry Logic**: Robust error handling with exponential backoff
- 📊 **Comprehensive Logging**: Detailed logs for debugging
- 🧪 **Fully Tested**: Unit tests and integration tests included

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Flask API Endpoint              │
│         POST /api/deploy                │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         API Handler Module              │
│   • Validates requests                  │
│   • Routes to Build/Revise              │
└────────────────┬────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐   ┌──────────────┐
│ LLM Module   │   │ Database     │
│ • Gemini     │   │ • Tasks      │
│ • OpenAI     │   │ • Deployments│
│ • Claude     │   └──────────────┘
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ GitHub Automation    │
│ • Create repos       │
│ • Upload files       │
│ • Enable Pages       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Evaluation Notifier  │
│ • POST metadata      │
│ • Retry logic        │
└──────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [UV package manager](https://github.com/astral-sh/uv)
- GitHub account with Personal Access Token
- LLM API key (Gemini recommended for free tier)

### Installation

```bash
# 1. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Clone repository
git clone <your-repo-url>
cd llm-code-deployer

# 3. Create folder structure
mkdir -p modules database utils prompts tests logs
touch modules/__init__.py database/__init__.py utils/__init__.py prompts/__init__.py tests/__init__.py

# 4. Create virtual environment
uv venv
source .venv/bin/activate  # Mac/Linux
# OR .venv\Scripts\activate  # Windows

# 5. Install dependencies
uv pip install -e .

# 6. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 7. Run tests
python run_tests.py

# 8. Start server
python app.py
```

Server will be available at `http://localhost:7860`

## 📝 API Usage

### Health Check

```bash
curl http://localhost:7860/
```

Response:
```json
{
  "status": "online",
  "service": "LLM Code Deployer",
  "version": "1.0.0",
  "llm_provider": "gemini"
}
```

### Deploy Application (Round 1)

```bash
curl -X POST http://localhost:7860/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "secret": "your-shared-secret",
    "task": "hello-world-001",
    "round": 1,
    "nonce": "unique-nonce-123",
    "brief": "Create a Bootstrap 5 page with a centered Hello World heading and a button that shows an alert",
    "checks": [
      "Page has Bootstrap 5 loaded",
      "h1 contains Hello World",
      "Button shows alert on click"
    ],
    "evaluation_url": "https://your-evaluation-api.com/notify",
    "attachments": []
  }'
```

Response:
```json
{
  "status": "success",
  "round": 1,
  "repo_url": "https://github.com/your-username/hello-world-001",
  "pages_url": "https://your-username.github.io/hello-world-001/",
  "commit_sha": "abc123def456..."
}
```

### Revise Application (Round 2)

```bash
curl -X POST http://localhost:7860/api/deploy \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "secret": "your-shared-secret",
    "task": "hello-world-001",
    "round": 2,
    "nonce": "unique-nonce-456",
    "brief": "Add a dark mode toggle button that switches between light and dark themes",
    "checks": [
      "Button with id=theme-toggle exists",
      "Clicking toggles dark mode",
      "Original features still work"
    ],
    "evaluation_url": "https://your-evaluation-api.com/notify",
    "attachments": []
  }'
```

### Check Deployment Status

```bash
curl http://localhost:7860/api/status/student@example.com/hello-world-001
```

Response:
```json
{
  "email": "student@example.com",
  "task_id": "hello-world-001",
  "round1": {
    "timestamp": "2024-01-15 10:30:00",
    "repo_url": "https://github.com/user/hello-world-001",
    "pages_url": "https://user.github.io/hello-world-001/",
    "commit_sha": "abc123..."
  },
  "round2": {
    "timestamp": "2024-01-15 11:45:00",
    "repo_url": "https://github.com/user/hello-world-001",
    "pages_url": "https://user.github.io/hello-world-001/",
    "commit_sha": "def456..."
  }
}
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following:

```env
# Student Authentication
STUDENT_SECRET=your-shared-secret-from-google-form

# LLM Configuration (choose one)
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key
# OPENAI_API_KEY=your-openai-key
# ANTHROPIC_API_KEY=your-claude-key

# GitHub Configuration
GITHUB_TOKEN=your-github-personal-access-token
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

### Getting API Keys

**GitHub Personal Access Token:**
1. Go to [GitHub Settings → Tokens](https://github.com/settings/tokens)
2. Generate new token (classic)
3. Select scopes: `repo`, `workflow`, `admin:repo_hook`

**Gemini API Key (Free):**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"

**OpenAI API Key (Paid):**
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Requires billing setup

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get running in 10 minutes
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Comprehensive setup tutorial
- **[API_REFERENCE.md](API_REFERENCE.md)** - API endpoint details

## 🧪 Testing

### Run All Tests

```bash
python run_tests.py
```

### Run Unit Tests

```bash
pytest tests/ -v
```

### Test Individual Modules

```bash
# Test configuration
python config.py

# Test database
python -c "from database.models import Database; db = Database(); print('OK')"

# Test LLM
python -c "from modules.llm_integration import LLMIntegration; llm = LLMIntegration(); print('OK')"

# Test GitHub
python -c "from modules.github_automation import GitHubAutomation; gh = GitHubAutomation(); print('OK')"
```

### Test with Sample Payloads

```bash
# Edit tests/sample_payloads.json with your credentials
# Then run:
python test_with_samples.py
```

## 🌐 Deployment

### Deploy to Hugging Face Spaces

1. **Create Space:**
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Create new Space with Docker SDK

2. **Add Files:**
   ```bash
   # Create requirements.txt
   uv pip freeze > requirements.txt
   
   # Create Dockerfile
   # (See SETUP_GUIDE.md Part 8)
   ```

3. **Configure Secrets:**
   - In Space settings, add all `.env` variables as secrets

4. **Push Code:**
   ```bash
   git remote add hf https://huggingface.co/spaces/USERNAME/SPACE-NAME
   git push hf main
   ```

### Deploy to Other Platforms

- **Heroku**: Use `Procfile` with `web: python app.py`
- **Railway**: Direct GitHub integration
- **Render**: Web service with Python environment
- **AWS/GCP/Azure**: Container deployment

## 🏗️ Project Structure

```
llm-code-deployer/
├── app.py                      # Main Flask application
├── config.py                   # Configuration management
├── pyproject.toml             # UV project configuration
├── .env                       # Environment variables (not in git)
├── .gitignore                 # Git ignore rules
│
├── modules/                   # Core application modules
│   ├── api_handler.py        # Request orchestration
│   ├── llm_integration.py    # LLM interface
│   ├── github_automation.py  # GitHub operations
│   └── evaluation_notifier.py # Evaluation API
│
├── database/                  # Database layer
│   └── models.py             # SQLite models
│
├── utils/                     # Utility functions
│   ├── validators.py         # Input validation
│   ├── logger.py             # Logging setup
│   └── helpers.py            # Helper functions
│
├── prompts/                   # LLM prompts
│   ├── code_generation.py    # Round 1 prompts
│   └── code_revision.py      # Round 2 prompts
│
├── tests/                     # Test suite
│   ├── test_api_handler.py   # Unit tests
│   └── sample_payloads.json  # Test data
│
└── logs/                      # Application logs
    └── app.log               # Main log file
```

## 🔍 How It Works

### Round 1: Build

1. **Receive Request** - Validate payload and authenticate
2. **Generate Code** - LLM creates HTML + README based on brief
3. **Create Repository** - Initialize GitHub repo with MIT license
4. **Upload Files** - Push `index.html`, `README.md`, `LICENSE`
5. **Enable Pages** - Configure GitHub Pages deployment
6. **Save State** - Store deployment info in database
7. **Notify Evaluator** - POST metadata to evaluation API

### Round 2: Revise

1. **Receive Request** - Validate and check for Round 1
2. **Retrieve Code** - Fetch existing code from database or GitHub
3. **Generate Updates** - LLM modifies code based on new requirements
4. **Update Repository** - Push changes to existing repo
5. **Save State** - Store Round 2 deployment info
6. **Notify Evaluator** - POST updated metadata

## 🎯 Use Cases

### Educational Assessments
- Automated code generation for student projects
- Revision workflows for iterative development
- Standardized evaluation across cohorts

### Rapid Prototyping
- Quick generation of proof-of-concept applications
- Iterative refinement based on feedback
- Instant deployment to shareable URLs

### Code Generation Platforms
- Backend for code generation services
- Integration with learning management systems
- API for automated web development

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

**Configuration errors:**
```bash
# Verify all required variables are set
python config.py
```

**LLM API errors:**
- Check API key validity
- Verify quota/billing status
- Review logs: `tail -f logs/app.log`

**GitHub API rate limits:**
- Wait 1 hour for reset
- Use authenticated requests
- Check limits: https://github.com/settings/tokens

**GitHub Pages not accessible:**
- Wait 2-3 minutes for build
- Check repo Settings → Pages
- Verify `index.html` exists

### Getting Help

- 📖 Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
- 🐛 Check [GitHub Issues](issues) for known problems
- 💬 Open a new issue for bug reports
- 📧 Contact: your-email@example.com

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [PyGithub](https://github.com/PyGithub/PyGithub) - GitHub API
- [Google Gemini](https://ai.google.dev/) - LLM provider
- [UV](https://github.com/astral-sh/uv) - Package manager

## 📊 Stats

- **Language:** Python 3.10+
- **Framework:** Flask 3.0+
- **Database:** SQLite
- **API:** REST
- **Deployment:** GitHub Pages
- **Testing:** pytest

## 🗺️ Roadmap

- [ ] Add Claude API support
- [ ] Implement caching for repeated requests
- [ ] Add email notifications
- [ ] Create web dashboard
- [ ] Support multiple file uploads
- [ ] Add code quality metrics
- [ ] Implement rate limiting
- [ ] Add webhook support

## 📞 Contact

- **Author:** Your Name
- **Email:** your.email@example.com
- **GitHub:** [@yourusername](https://github.com/yourusername)
- **Twitter:** [@yourhandle](https://twitter.com/yourhandle)

---

<div align="center">

Made with ❤️ by developers, for developers

⭐ Star this repo if you find it helpful!

</div>
```