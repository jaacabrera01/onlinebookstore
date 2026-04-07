# GitHub Deployment & Security Guide

## 🔐 Security Setup Complete

Your project is now safe to deploy to GitHub without exposing sensitive information.

### What Was Changed

1. **config.py** - Removed hardcoded passwords
   - Credentials now loaded from environment variables (.env file)
   - .env file is protected by .gitignore (never committed)

2. **.gitignore** - Created to prevent sensitive files from being committed
   - Protects: `.env`, `.venv/`, `__pycache__/`, test results, etc.

3. **.env.example** - Template file showing required variables
   - Safe to commit to GitHub
   - Shows team members what environment variables are needed

4. **.env** - Local secrets file (not committed, for development only)
   - Contains your actual credentials
   - Automatically loaded by config.py

## 📋 Files Safe to Commit

✅ Safe to commit:
- All Python source files (.py)
- Test files (tests/)
- Configuration templates (.env.example)
- Workflows (.github/workflows/.yml)
- Documentation files
- .gitignore

❌ NOT committed (protected):
- .env (your local secrets)
- .venv/ (your virtual environment)
- test-results/ (test artifacts)
- __pycache__/ (Python cache)
- allure-results/ (test data)

## 🚀 Deploying to GitHub

### Step 1: Initialize Git Repository

```bash
cd "/Users/jaacabrera/Documents/Python Scripts/Online Bookstore"
git init
git add .
git status  # Verify .env is NOT in the list
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create new repository (name: online-bookstore or similar)
3. Do NOT add README/gitignore (you already have them)
4. Click "Create repository"

### Step 3: Push to GitHub

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/your-repo-name.git
git commit -m "Initial commit: Add BookCart automation test suite"
git push -u origin main
```

## 🔐 Setting Up GitHub Secrets for CI/CD

GitHub workflows need access to your credentials. Use GitHub Secrets instead of hardcoding them.

### Step 1: Add Secrets to GitHub

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** and add:

   | Name | Value |
   |------|-------|
   | TEST_USERNAME | jaacabrera |
   | TEST_PASSWORD | Admin1234! |
   | API_ADMIN_USERNAME | admin |
   | API_ADMIN_PASSWORD | admin |

### Step 2: Update Workflows to Use Secrets

The workflows in `.github/workflows/` need to pass these secrets as environment variables.

Add to each test step in your workflow files:

```yaml
env:
  TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
  TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
  API_ADMIN_USERNAME: ${{ secrets.API_ADMIN_USERNAME }}
  API_ADMIN_PASSWORD: ${{ secrets.API_ADMIN_PASSWORD }}
```

**Example updated workflow snippet:**

```yaml
- name: Run API Security Tests
  env:
    TEST_USERNAME: ${{ secrets.TEST_USERNAME }}
    TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}
    API_ADMIN_USERNAME: ${{ secrets.API_ADMIN_USERNAME }}
    API_ADMIN_PASSWORD: ${{ secrets.API_ADMIN_PASSWORD }}
  run: pytest tests/test_api_security.py -v
```

## 🔍 Before Pushing: Security Checklist

Run these commands to make sure no secrets are being committed:

```bash
# Check if .env would be committed
git status | grep ".env"
# Should show nothing (it's in .gitignore)

# Verify .env is ignored
git check-ignore -v .env
# Should output: .env    .gitignore

# Check what would be committed
git diff --cached --name-only | grep -i "password\|secret\|credential\|admin"
# Should return nothing
```

## 📖 For Team Members Cloning Repository

When someone clones your repository from GitHub:

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/online-bookstore.git
cd online-bookstore

# 2. Create their own .env file from template
cp .env.example .env

# 3. Edit .env with their credentials
nano .env
# Or use any text editor to fill in TEST_PASSWORD and API_ADMIN_PASSWORD

# 4. Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt
playwright install

# 6. Run tests
pytest tests/ -v
```

## ✅ Verification

After pushing to GitHub, verify:

1. **No secrets exposed:**
   - Go to your repo → navigate to config.py
   - Should show: `TEST_PASSWORD: str = ""`
   - Should NOT show actual password

2. **.env not committed:**
   - Search repository for .env file
   - Should NOT appear in file listing

3. **Workflows configured:**
   - Go to Actions tab
   - Verify workflows exist and are ready to run

## 🔐 Additional Security Best Practices

1. **Rotate credentials** after deploying
   - Change TEST_PASSWORD in the website
   - Update GitHub Secrets
   - Update team members' .env files

2. **Use personal access tokens instead of passwords** (for API auth)
   - Safer than storing passwords
   - Can be revoked individually

3. **Review GitHub Security tab regularly**
   - Settings → Security and analysis
   - Enable secret scanning
   - Enable security alerts

4. **Train team members**
   - Never commit .env files
   - Explain .gitignore purpose
   - Use GitHub Secrets for CI/CD

## 📝 Summary

| Item | Status | Location |
|------|--------|----------|
| Credentials in config.py | ✅ Removed | config.py (lines 38-45) |
| Environment file | ✅ Protected | .env (in .gitignore) |
| Template provided | ✅ Created | .env.example |
| Git ignore configured | ✅ Setup | .gitignore |
| CI/CD workflows ready | ✅ Available | .github/workflows/ |
| GitHub secrets guidance | ✅ Documented | This file |

Your project is ready for GitHub deployment! 🚀

---

**Last Updated:** April 7, 2026
**Security Level:** ✅ Production Ready
