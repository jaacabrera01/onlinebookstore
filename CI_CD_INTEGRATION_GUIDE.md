# CI/CD Integration Guide

## Overview

Your project now has GitHub Actions workflows that automatically run tests on every push and pull request. This ensures code quality and security is maintained continuously.

## Workflows

### 1. **Automated Tests** (`tests.yml`)
- **Trigger**: Every push to `main` or `develop` branches, and all pull requests
- **Duration**: ~5-10 minutes
- **Python Versions**: Tests run on Python 3.10 and 3.11 to ensure compatibility
- **What it does**:
  - Installs all dependencies
  - Installs Playwright browsers for UI tests
  - Runs all 11 test suites (security, authentication, checkout, etc.)
  - Generates Allure test reports
  - Uploads test results as artifacts

### 2. **Smoke Tests** (`smoke-tests.yml`)
- **Trigger**: Every push to `main` or `develop` branches, and all pull requests
- **Duration**: ~2-3 minutes (faster)
- **What it does**:
  - Runs only critical tests (API security, authentication, checkout, payment)
  - Quick feedback on core functionality
  - Good for rapid PR feedback

## How It Works

### Setup Requirements
The workflows automatically:
1. ✅ Check out your code
2. ✅ Set up Python environment
3. ✅ Install dependencies from `requirements.txt`
4. ✅ Install Playwright browsers
5. ✅ Run all test suites
6. ✅ Generate reports and artifacts

### No Additional Setup Needed!
Since you're using GitHub, the workflows will run automatically once committed. No API keys or additional configuration required.

## Viewing Results

### On GitHub
1. Go to your repository
2. Click the **Actions** tab
3. View the latest workflow run
4. Check which tests passed/failed
5. Download artifacts (test results, Allure reports)

### Artifacts
After each run, you can download:
- **allure-results-3.10** - Test result data for Python 3.10
- **allure-results-3.11** - Test result data for Python 3.11
- **allure-report-3.10** - Full Allure HTML report for Python 3.10
- **allure-report-3.11** - Full Allure HTML report for Python 3.11

To view an Allure report locally:
```bash
# Extract the downloaded artifact, then:
allure serve path/to/allure-results
```

## Test Suites Included

The workflows run these test suites in sequence:
1. **test_api_security.py** - REST API security validation
2. **test_authorization_security.py** - Access control and privilege escalation
3. **test_payment_security.py** - Payment processing and PCI compliance
4. **test_security_comprehensive.py** - Core security (SQL injection, XSS, CSRF, etc.)
5. **test_authentication.py** - User login/logout flows
6. **test_shopping_cart.py** - Cart operations
7. **test_checkout.py** - Checkout flows
8. **test_product_search.py** - Product search functionality
9. **test_api.py** - General API tests
10. **test_visual_regression.py** - UI visual regression tests

## Customization

### To modify trigger branches
Edit `tests.yml` and `smoke-tests.yml`:
```yaml
on:
  push:
    branches: [ main, develop, feature-* ]  # Add branches here
  pull_request:
    branches: [ main, develop ]
```

### To add more Python versions
Edit `tests.yml`:
```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12']  # Add versions
```

### To change which tests run
Edit the test steps in either workflow file to include/exclude specific test files.

### To add Slack/Email notifications
Add a step at the end:
```yaml
- name: Send Slack notification
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
```

## Troubleshooting

### Workflow fails with "playwright install" error
- Update `requirements.txt` to ensure `playwright>=1.40.0` is pinned
- The `playwright install` step installs browser binaries

### Tests pass locally but fail on GitHub
- Ensure `config.py` uses environment variables for base URLs
- GitHub runners may have different network access
- Check if tests need headless mode (they should by default)

### Artifacts not appearing
- Check if the test suite failed before artifacts were generated
- Look at the workflow logs to see which step failed

## Next Steps

1. **Push to GitHub**: Commit and push these workflow files to your `main` or `develop` branch
2. **Monitor Actions tab**: Watch the workflows run automatically
3. **Review reports**: Download and review Allure reports for detailed test results
4. **Integrate with PR checks**: GitHub will automatically check PR quality with test results
5. **Set branch protection**: Require tests to pass before merging PRs (in GitHub Settings)

## Local Testing vs CI/CD

| Aspect | Local | CI/CD |
|--------|-------|-------|
| **Speed** | Instant feedback | 5-10 minutes |
| **Frequency** | When you run tests | Every commit |
| **Environment** | Your machine | Isolated runner |
| **Python versions** | One version | Multiple versions |
| **History** | Not tracked | Full history stored |
| **Reporting** | Console output | Artifacts + GitHub UI |

## Branch Protection Rule (Optional but Recommended)

In GitHub repository settings:
1. Go to **Settings** > **Branches**
2. Add rule for `main` branch
3. Check "Require status checks to pass before merging"
4. Select both "Automated Tests" and "Smoke Tests"
5. This prevents merging if tests fail

---

**Your CI/CD pipeline is now live!** 🚀 All commits will automatically trigger test runs.
