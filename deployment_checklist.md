# ✅ Deployment Checklist

Use this checklist before deploying to production.

## 📋 Pre-Deployment Checklist

### 1. Environment Setup

- [ ] Python 3.10+ installed
- [ ] UV package manager installed
- [ ] Virtual environment created and activated
- [ ] All dependencies installed via `uv pip install -e .`
- [ ] `.env` file created from `.env.example`
- [ ] All required environment variables set

### 2. API Keys & Credentials

- [ ] GitHub Personal Access Token obtained
- [ ] GitHub token has correct scopes (`repo`, `workflow`, `admin:repo_hook`)
- [ ] LLM API key obtained (Gemini/OpenAI/Claude)
- [ ] LLM API key tested and working
- [ ] STUDENT_SECRET set to a strong, unique value
- [ ] All secrets stored securely (never in code)

### 3. Configuration Validation

- [ ] `python config.py` runs without errors
- [ ] LLM_PROVIDER matches available API key
- [ ] GITHUB_USERNAME is correct
- [ ] DATABASE_PATH is writable
- [ ] LOG_FILE path exists and is writable

### 4. Module Testing

- [ ] Configuration test passes
- [ ] Database initialization works
- [ ] LLM integration test succeeds
- [ ] GitHub authentication works
- [ ] Can list GitHub repositories
- [ ] Evaluation notifier configured

### 5. Integration Testing

- [ ] `pytest tests/ -v` passes all tests
- [ ] `python run_tests.py` completes successfully
- [ ] Flask server starts without errors
- [ ] Health endpoint returns 200 OK
- [ ] Sample payload test succeeds

### 6. Security Review

- [ ] `.env` file in `.gitignore`
- [ ] No API keys in code
- [ ] No secrets in git history
- [ ] STUDENT_SECRET is strong (16+ characters)
- [ ] GitHub token permissions minimized
- [ ] Logs don't contain sensitive data

### 7. GitHub Repository

- [ ] MIT LICENSE file exists
- [ ] README.md is complete
- [ ] .gitignore properly configured
- [ ] No sensitive files in repository
- [ ] All required files committed

### 8. Database

- [ ] Database directory exists
- [ ] Database initializes correctly
- [ ] Can insert and retrieve records
- [ ] Database path is not in git

### 9. Logging

- [ ] Logs directory exists
- [ ] Log file is writable
- [ ] Log level appropriate (INFO for production)
- [ ] Logs are readable and informative

### 10. Error Handling

- [ ] Invalid requests return proper errors
- [ ] Secret validation works
- [ ] GitHub API errors handled gracefully
- [ ] LLM API errors handled gracefully
- [ ] Retry logic configured and tested

---

## 🚀 Hugging Face Spaces Deployment

### Pre-Deployment

- [ ] Hugging Face account created
- [ ] Space created with Docker SDK
- [ ] `requirements.txt` generated via `uv pip freeze`
- [ ] `Dockerfile` created
- [ ] README with Space metadata created

### Configuration

- [ ] All environment variables added as Space secrets
- [ ] No sensitive data in repository
- [ ] PORT set to 7860 (Hugging Face default)
- [ ] FLASK_ENV set to production

### Testing on Spaces

- [ ] Space builds successfully
- [ ] No build errors in logs
- [ ] Health endpoint accessible
- [ ] Can make POST request to /api/deploy
- [ ] GitHub integration works from Spaces
- [ ] LLM API works from Spaces

---

## 🧪 Production Readiness

### Performance

- [ ] Response time acceptable (< 2 minutes)
- [ ] Database queries optimized
- [ ] LLM timeouts configured
- [ ] GitHub API rate limits understood
- [ ] Concurrent request handling tested

### Monitoring

- [ ] Log rotation configured
- [ ] Disk space monitored
- [ ] Error alerting configured (optional)
- [ ] Usage metrics tracked (optional)

### Documentation

- [ ] API endpoints documented
- [ ] Setup guide complete
- [ ] Troubleshooting guide available
- [ ] Example payloads provided
- [ ] Response formats documented

### Backup & Recovery

- [ ] Database backup strategy defined
- [ ] Can restore from backup
- [ ] Deployment rollback plan exists
- [ ] Git tags for versions

---

## 📊 Post-Deployment Verification

### Immediate Checks (First 5 Minutes)

- [ ] Service is running
- [ ] Health endpoint returns 200
- [ ] Can authenticate with secret
- [ ] Test Round 1 deployment works
- [ ] GitHub repo created successfully
- [ ] GitHub Pages accessible
- [ ] Evaluation API notification sent

### Extended Checks (First Hour)

- [ ] Test Round 2 revision works
- [ ] Existing repo updated correctly
- [ ] Multiple requests handled
- [ ] Error cases handled properly
- [ ] Logs are being written
- [ ] No memory leaks observed

### Long-Term Monitoring (First Week)

- [ ] Track successful deployments
- [ ] Monitor failure rates
- [ ] Check GitHub API quota usage
- [ ] Monitor LLM API costs
- [ ] Review error logs daily
- [ ] Verify evaluation notifications

---

## 🐛 Common Issues Checklist

### If Deployment Fails

- [ ] Check `.env` file exists and is complete
- [ ] Verify all API keys are valid
- [ ] Check GitHub token permissions
- [ ] Review logs for errors: `tail -f logs/app.log`
- [ ] Test LLM API independently
- [ ] Test GitHub API independently
- [ ] Verify network connectivity
- [ ] Check disk space availability

### If Round 2 Fails

- [ ] Verify Round 1 completed successfully
- [ ] Check database for Round 1 entry
- [ ] Try fetching repo from GitHub
- [ ] Verify repo name matches task ID
- [ ] Check GitHub repo permissions
- [ ] Review LLM revision prompt
- [ ] Verify existing code is valid HTML

### If GitHub Pages Not Accessible

- [ ] Wait 2-3 minutes for build
- [ ] Check repo Settings → Pages
- [ ] Verify `index.html` exists in root
- [ ] Check file is valid HTML
- [ ] Verify repo is public
- [ ] Check GitHub Pages status page

### If Evaluation API Fails

- [ ] Verify evaluation_url is correct
- [ ] Check network connectivity
- [ ] Review retry logic configuration
- [ ] Check evaluation API is online
- [ ] Verify payload format is correct
- [ ] Review timeout settings

---

## ✅ Final Sign-Off

Before going live:

- [ ] All above checks completed
- [ ] Test deployment successful
- [ ] Team/instructor notified
- [ ] Documentation shared
- [ ] Support plan in place
- [ ] Monitoring active

**Deployed by:** ________________

**Date:** ________________

**Version:** ________________

**Environment:** ☐ Development ☐ Staging ☐ Production

**Notes:**
_______________________________________
_______________________________________
_______________________________________

---

## 📞 Emergency Contacts

**Technical Issues:**
- Your Name: your.email@example.com
- Phone: +1-xxx-xxx-xxxx

**API Issues:**
- GitHub Support: https://support.github.com
- Gemini Support: https://ai.google.dev/support
- OpenAI Support: https://help.openai.com

**Platform Issues:**
- Hugging Face Support: https://huggingface.co/support

---

## 🔄 Rollback Plan

If critical issues occur:

1. **Stop Service:**
   ```bash
   # Kill the process or pause Space
   ```

2. **Revert to Previous Version:**
   ```bash
   git revert HEAD
   git push
   ```

3. **Restore Database (if needed):**
   ```bash
   cp database/deployments.db.backup database/deployments.db
   ```

4. **Notify Users:**
   - Email affected users
   - Post status update
   - Provide timeline

5. **Root Cause Analysis:**
   - Review logs
   - Identify issue
   - Fix and test
   - Redeploy

---

**🎉 Good luck with your deployment!**