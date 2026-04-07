# Security Test Suite - Quick Start Guide

## Installation & Setup

### 1. Activate Python Environment
```bash
cd "/Users/jaacabrera/Documents/Python Scripts/Online Bookstore"
source .venv/bin/activate
```

### 2. Install/Update Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
pytest --version
playwright --version
```

## Quick Commands

### Run All Security Tests
```bash
pytest tests/test_security_comprehensive.py \
        tests/test_api_security.py \
        tests/test_authorization_security.py \
        tests/test_payment_security.py \
        tests/test_data_validation.py \
        -v
```

### Run Specific Test Category

**SQL Injection Tests**
```bash
pytest tests/test_security_comprehensive.py::TestSQLInjectionPrevention -v
```

**XSS Prevention Tests**
```bash
pytest tests/test_security_comprehensive.py::TestXSSPrevention -v
```

**Authentication Security Tests**
```bash
pytest tests/test_security_comprehensive.py::TestAuthenticationSecurity -v
```

**API Security Tests**
```bash
pytest tests/test_api_security.py -v
```

**Authorization Tests**
```bash
pytest tests/test_authorization_security.py -v
```

**Payment Security Tests**
```bash
pytest tests/test_payment_security.py -v
```

**Data Validation Tests**
```bash
pytest tests/test_data_validation.py -v
```

### Run Tests with Markers

**All Security Tests**
```bash
pytest -m "security" -v
```

**Critical Only**
```bash
pytest -m "critical" -v
```

**API Tests Only**
```bash
pytest -m "api" -v
```

**Payment Tests Only**
```bash
pytest -m "payment" -v
```

**Data Validation Only**
```bash
pytest -m "data_validation" -v
```

### Run Single Test with Verbose Output
```bash
pytest tests/test_security_comprehensive.py::TestSQLInjectionPrevention::test_sql_injection_in_login_username -vvs
```

### Run Tests and Generate Allure Report
```bash
pytest tests/test_security_comprehensive.py \
        tests/test_api_security.py \
        tests/test_authorization_security.py \
        tests/test_payment_security.py \
        tests/test_data_validation.py \
        -v --alluredir=allure-results

# View report
allure serve allure-results
```

### Run Tests with HTML Report
```bash
pytest tests/test_security_*.py -v --html=report.html --self-contained-html
# Open: report.html in browser
```

### Run Tests with Coverage Report
```bash
pytest tests/test_security_*.py \
        --cov=pages \
        --cov=utils \
        --cov-report=html \
        --cov-report=term
# Open: htmlcov/index.html for detailed coverage
```

## Test Statistics

### Total Tests Available
- **SQL Injection Prevention**: 2 tests
- **XSS Prevention**: 3 tests
- **Authentication Security**: 3 tests
- **Session Security**: 3 tests
- **Input Validation**: 3 tests
- **Information Disclosure**: 3 tests
- **CSRF Protection**: 2 tests
- **API Authentication**: 2 tests
- **API Authorization**: 2 tests
- **API Rate Limiting**: 1 test
- **API Input Validation**: 2 tests
- **API Response Security**: 3 tests
- **API Endpoint Coverage**: 1 test
- **Access Control**: 3 tests
- **Privilege Escalation**: 2 tests
- **Resource Ownership**: 2 tests
- **Session Authorization**: 2 tests
- **Price Integrity**: 2 tests
- **Quantity Tampering**: 1 test
- **Discount Validation**: 2 tests
- **Checkout Security**: 2 tests
- **Order Integrity**: 2 tests
- **PCI Compliance**: 2 tests
- **Transaction Validation**: 2 tests
- **Boundary Testing**: 3 tests
- **Special Characters**: 2 tests
- **Type Validation**: 3 tests
- **Regex Bypass**: 1 test
- **File Upload Security**: 2 tests
- **Whitelist Validation**: 2 tests

**Total: 65+ Security Tests**

## Expected Results

### Healthy Application Signs
```
✅ PASSED: Prevent SQL Injection in Login Username Field
✅ PASSED: Prevent Stored XSS in Product Reviews
✅ PASSED: Prevent Authentication Bypass with Empty Credentials
✅ PASSED: Verify Secure Session Cookie Flags
✅ PASSED: Prevent API Access Without Authentication
✅ PASSED: Prevent Access to Admin Pages Without Role
✅ PASSED: Verify Order Total Cannot Be Modified
...and more
```

### Issues to Watch For
```
❌ FAILED: SQL injection payload was accepted
❌ FAILED: XSS script executed on page
❌ FAILED: Admin page accessible without admin role
❌ FAILED: User can access other users' orders
❌ FAILED: Price can be modified before purchase
```

## Common Issues & Solutions

### "Command not found: pytest"
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Or use python module syntax
python -m pytest tests/test_security_comprehensive.py -v
```

### "Module not found: playwright"
```bash
# Install missing dependencies
pip install playwright

# Install browsers
playwright install
```

### Tests Timeout/Hang
```bash
# Set timeout (seconds)
pytest tests/test_security_comprehensive.py --timeout=30 -v

# Or kill and restart
pkill -f playwright
```

### HTTPS Certificate Errors
```bash
# Some tests may need to ignore certificate verification
# This is often okay for testing against self-signed certs

# Or check if BASE_URL in config.py is correct
python -c "from config import get_settings; print(get_settings().BASE_URL)"
```

### Can't Connect to Website
```bash
# Verify website is running
curl https://bookcart.azurewebsites.net/

# Check internet connection
ping google.com

# Try pinging the website
ping bookcart.azurewebsites.net
```

## Select Tests to Run

### Quick Smoke Test (2-3 minutes)
```bash
pytest tests/test_security_comprehensive.py::TestAuthenticationSecurity::test_empty_credentials_rejection \
        tests/test_security_comprehensive.py::TestSQLInjectionPrevention::test_sql_injection_in_login_username \
        tests/test_security_comprehensive.py::TestXSSPrevention::test_xss_in_login_parameter \
        -v
```

### Full Security Audit (15-20 minutes)
```bash
pytest tests/test_security_comprehensive.py \
        tests/test_api_security.py \
        tests/test_authorization_security.py \
        tests/test_payment_security.py \
        tests/test_data_validation.py \
        -v --tb=short
```

### Just API Security (5 minutes)
```bash
pytest tests/test_api_security.py -v
```

### Just Payment Security (3 minutes)
```bash
pytest tests/test_payment_security.py -v
```

## Test Output Interpretation

### PASSED ✅
- Test condition was met successfully
- Application properly handles the security scenario
- No vulnerability detected

### FAILED ❌
- Test condition was not met
- Potential security vulnerability exists
- Requires investigation and fix

### SKIPPED ⊘
- Test was not executed (expected)
- Usually due to missing test data or optional features
- Not a problem unless unexpected

### ERROR ⚠️
- Test couldn't run due to technical issue
- Browser/connection issue or test configuration problem
- Check test output for details

## Continuous Integration

### Add to GitHub Actions
```yaml
name: Security Tests

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: playwright install
      - run: pytest tests/test_security_*.py -v --tb=short
```

### Add to Pre-commit Hooks
```bash
# Create .git/hooks/pre-commit
#!/bin/bash
echo "Running security tests before commit..."
pytest tests/test_security_comprehensive.py -q
if [ $? -ne 0 ]; then
    echo "Security tests failed!"
    exit 1
fi
```

## Performance Tips

1. **Run tests in parallel** (requires pytest-xdist)
   ```bash
   pip install pytest-xdist
   pytest tests/ -n auto -v
   ```

2. **Skip slow tests temporarily**
   ```bash
   pytest tests/ -v --ignore=tests/test_api_security.py
   ```

3. **Run only modified tests**
   ```bash
   pytest tests/ --lf -v  # last failed
   pytest tests/ --ff -v  # failed first
   ```

## Next Steps

1. **Review Detailed Test Documentation**
   - Read: [SECURITY_TEST_SUITE_README.md](SECURITY_TEST_SUITE_README.md)

2. **Configure for Your Environment**
   - Update `config.py` with your API endpoints
   - Set environment variables if needed

3. **Integrate into CI/CD**
   - Add to GitHub Actions/Jenkins
   - Set up nightly test runs
   - Enable test reports

4. **Customize Test Data**
   - Add your own test users
   - Configure test data for your environment
   - Update test payloads as needed

5. **Monitor Security**
   - Run tests regularly
   - Review failed tests carefully
   - Fix vulnerabilities promptly
   - Keep tests updated

## Support & Help

**Quick troubleshooting:**
```bash
# Show all available markers
pytest --markers | grep -i security

# List all security tests without running
pytest tests/test_security_*.py --collect-only -q

# Run with maximum verbosity
pytest tests/test_security_comprehensive.py::TestSQLInjectionPrevention -vvv
```

**Get help:**
- Check test docstrings: `pytest --collect-only -q tests/test_security_comprehensive.py`
- Read test source code comments
- Review error output carefully
- Check Allure report for visual debugging

---

**Ready to test?** Start with:
```bash
pytest tests/test_security_comprehensive.py -v
```

Good luck! 🚀🔒
