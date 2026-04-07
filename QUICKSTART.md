# Quick Start Guide

## 5-Minute Setup

### 1. Install Python dependencies:
```bash
pip install -r requirements.txt
playwright install
```

### 2. Run your first test:
```bash
pytest tests/test_authentication.py -v
```

### 3. View results:
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

---

## Common Commands

### Run all tests
```bash
pytest tests/ -v
```

### Run only critical path tests (5 minutes)
```bash
pytest -m critical -v
```

### Run only smoke tests (quick check)
```bash
pytest -m smoke -v
```

### Run specific test file
```bash
pytest tests/test_authentication.py -v
```

### Run with detailed output
```bash
pytest tests/ -v -s
```

### Run in headed mode (see browser)
Update `.env` or use:
```bash
pytest tests/ -v --headed
```

### Run on specific browser
```bash
pytest tests/ -v --browser firefox
```

### Run tests in parallel
```bash
pytest tests/ -v -n auto
```

### View test report
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### See coverage
```bash
pytest tests/ --cov=pages --cov=utils --cov-report=html
open htmlcov/index.html
```

---

## Test Organization Cheat Sheet

| Command | Purpose | Duration |
|---------|---------|----------|
| `pytest -m smoke` | Quick sanity check | 2-3 min |
| `pytest -m critical` | Critical paths only | 5-10 min |
| `pytest -m regression` | Full test suite | 30+ min |
| `pytest tests/test_authentication.py` | Auth tests only | 5 min |
| `pytest tests/ -m "not slow"` | Exclude slow tests | 20 min |

---

## Troubleshooting

### Tests won't run
```bash
# Check Python version (need 3.10+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Reinstall browsers
playwright install --with-deps
```

### Element not found errors
1. Check the element exists in target page
2. Try waiting longer:
   ```bash
   WAIT_TIMEOUT=20000 pytest tests/test_file.py -v
   ```
3. Update selector in page object if page HTML changed

### Tests pass locally but fail in CI
1. Check `.env` variables match CI environment
2. Ensure BASE_URL is correct
3. Check for hardcoded waits or timing assumptions

### Need to debug a test
```bash
# Run with detailed output
pytest tests/test_file.py::TestClass::test_method -v -s

# Enter debugger on failure
pytest tests/ --pdb

# Keep browser open after test
HEADED=true pytest tests/ -v
```

---

## Writing Your First Test

1. **Choose a page** from `pages/` directory (or create new one)
2. **Create test file** in `tests/` directory:

```python
import pytest
from pages.login_page import LoginPage

class TestMyFeature:
    @pytest.mark.critical
    async def test_my_feature(self, page):
        login_page = LoginPage(page)
        
        # Go to page
        await login_page.goto_login()
        
        # Do something
        await login_page.login("user@example.com", "password")
        
        # Check result
        assert "home" in (await login_page.get_url()).lower()
```

3. **Run your test**:
```bash
pytest tests/test_your_file.py::TestMyFeature::test_my_feature -v -s
```

---

## Understanding Test Markers

```python
@pytest.mark.smoke      # Quick test of critical path
@pytest.mark.critical   # Important functionality
@pytest.mark.regression # Comprehensive testing
@pytest.mark.slow       # Takes longer to run
```

Run tests by category:
```bash
pytest -m smoke         # Just smoke tests
pytest -m critical      # Just critical tests
pytest -m "not slow"    # Skip long-running tests
```

---

## Next Steps

1. ✅ Run smoke tests to verify setup
2. ✅ Review test files in `tests/` directory
3. ✅ Examine page objects in `pages/` directory
4. ✅ Create your own test following the examples
5. ✅ Set up GitHub Actions workflow (see README.md)

---

## Need Help?

- 📖 See [README.md](README.md) for full documentation
- 🔍 Check test examples in `tests/` directory
- 📚 Review [Playwright docs](https://playwright.dev/python/)
- 🐛 Enable debug output: `pytest -v -s`
