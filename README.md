#Project URL: https://bookcart.azurewebsites.net
# BookCart Automation Testing Framework

A comprehensive test automation framework for the BookCart e-commerce application using Playwright and Python. This framework covers critical paths including user authentication, product search, shopping cart management, and checkout processes, with support for cross-browser testing, API testing, and visual regression testing.

## Features

🎯 **Critical Path Coverage**
- User authentication (login and registration)
- Product search and navigation
- Shopping cart management
- Checkout process
- API endpoint validation

🚀 **Advanced Testing Capabilities**
- Cross-browser testing (Chrome, Firefox, Safari/WebKit)
- Visual regression testing
- API testing layer
- CI/CD integration with GitHub Actions
- Comprehensive reporting with Allure Reports
- Dynamic element waiting (no fixed sleeps)
- Page Object Model pattern for maintainability

📊 **Quality Assurance**
- Data-driven testing with meaningful assertions
- Smart selector strategy (data-test-id preferred)
- Proper test isolation and cleanup
- Detailed logging and debugging
- Test categorization (smoke, regression, critical)

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Git (for version control)

## Installation

1. **Clone the repository** (if using git):
```bash
git clone <repository-url>
cd bookcart-automation
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install Playwright browsers**:
```bash
playwright install
python -m playwright install-deps
```

## Configuration

Create a `.env` file in the project root (optional, uses defaults if not provided):

```env
BASE_URL=https://bookcart.azurewebsites.net/
HEADLESS=true
SLOW_MO=0
BROWSERS=chromium,firefox,webkit
TIMEOUT=30000
NAVIGATION_TIMEOUT=30000
WAIT_TIMEOUT=10000
TEST_USERNAME=your-test-email@example.com
TEST_PASSWORD=your-test-password
SCREENSHOT_ON_FAILURE=true
```

## Project Structure

```
bookcart-automation/
├── config.py                    # Configuration management
├── conftest.py                  # Pytest fixtures and setup
├── pytest.ini                   # Pytest configuration
├── pyproject.toml               # Project metadata
├── requirements.txt             # Python dependencies
│
├── pages/                       # Page Object Models
│   ├── __init__.py             # Base page class
│   ├── home_page.py            # Homepage page object
│   ├── login_page.py           # Login page object
│   ├── register_page.py        # Registration page object
│   ├── product_detail_page.py  # Product details page object
│   ├── cart_page.py            # Shopping cart page object
│   └── checkout_page.py        # Checkout page object
│
├── utils/                       # Utility functions
│   ├── __init__.py             # Logging setup
│   ├── api_client.py           # API testing client
│   └── visual_regression.py    # Visual regression utilities
│
├── tests/                       # Test suites
│   ├── test_authentication.py  # Login and registration tests
│   ├── test_product_search.py  # Search and navigation tests
│   ├── test_shopping_cart.py   # Cart management tests
│   ├── test_checkout.py        # Checkout process tests
│   ├── test_api.py             # API endpoint tests
│   └── test_visual_regression.py # Visual regression tests
│
├── .github/
│   └── workflows/
│       ├── tests.yml           # Main test workflow
│       └── regression-tests.yml # Scheduled regression tests
│
└── test-results/               # Generated test artifacts
    ├── screenshots/
    └── logs/
```

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run specific test file:
```bash
pytest tests/test_authentication.py -v
```

### Run tests by marker:
```bash
# Smoke tests only
pytest -m smoke -v

# Critical tests only
pytest -m critical -v

# Regression tests only
pytest -m regression -v

# Exclude slow tests
pytest -m "not slow" -v
```

### Run tests with specific browser:
```bash
pytest tests/ -v --browsers chromium
pytest tests/ -v --browsers firefox
pytest tests/ -v --browsers webkit  # Safari-compatible
```

### Run tests in parallel:
```bash
pip install pytest-xdist
pytest tests/ -v -n auto
```

### Generate Allure Report:
```bash
pytest tests/ --alluredir=allure-results
allure serve allure-results
```

### Run with detailed output:
```bash
pytest tests/ -v -s
```

### Run with coverage:
```bash
pip install pytest-cov
pytest tests/ --cov=pages --cov=utils --cov-report=html
```

### Run API tests only:
```bash
pytest tests/test_api.py -v
```

### Run visual regression tests:
```bash
pytest tests/test_visual_regression.py -v
```

## Test Organization

### Test Categories

Tests are organized using pytest markers:

| Marker | Purpose | Example |
|--------|---------|---------|
| `@pytest.mark.smoke` | Critical path sanity tests | Login, add to cart, checkout |
| `@pytest.mark.critical` | High-priority functionality | Authentication, payment |
| `@pytest.mark.regression` | Comprehensive test coverage | All features |
| `@pytest.mark.slow` | Long-running tests | Visual regression |

### Running Specific Test Categories:

```bash
# Smoke tests (quick verification)
pytest -m smoke -v

# Critical path tests
pytest -m critical -v

# Full regression suite
pytest -m regression -v
```

## Writing New Tests

### 1. Create a new test file in `tests/` directory:

```python
"""Description of test module."""
import pytest
import allure
from pages.page_object import PageObject
from playwright.async_api import Page


@allure.feature("Feature Name")
@allure.suite("Test Suite")
class TestYourFeature:
    """Test class for feature."""
    
    @allure.title("Test Case Title")
    @allure.description("Detailed description")
    @pytest.mark.critical
    async def test_your_feature(self, page: Page):
        """Test implementation."""
        page_obj = PageObject(page)
        
        # Arrange
        await page_obj.goto_page()
        
        # Act
        await page_obj.perform_action()
        
        # Assert
        assert await page_obj.verify_result()
```

### 2. Use existing page objects:

```python
from pages.home_page import HomePage
from pages.login_page import LoginPage

async def test_login_flow(self, page: Page):
    login_page = LoginPage(page)
    
    await login_page.goto_login()
    await login_page.login("user@example.com", "password")
    # Verification
```

### 3. Add API tests:

```python
from utils.api_client import APIClient, assert_response

def test_api_endpoint(self):
    client = APIClient()
    response = client.get("api/products")
    assert_response(response, 200)
    client.close()
```

## Debugging Tests

### Take Screenshots on Failure:
Screenshots are automatically captured on test failure when `SCREENSHOT_ON_FAILURE=true` in config.

### View Test Execution Trace:
```bash
pytest tests/test_file.py -v --option record_trace=on
```

### Run single test with output:
```bash
pytest tests/test_file.py::TestClass::test_method -v -s
```

### Enable debug mode:
```bash
pytest tests/ -v --pdb  # Drop into debugger on failure
```

### Check logs:
```bash
tail -f logs/test_*.log
```

## Best Practices

### Selectors Strategy

✅ **DO** use data attributes:
```python
button = page.locator('[data-test-id="login-button"]')
```

✅ **DO** use user-facing text:
```python
button = page.locator('button:has-text("Login")')
```

❌ **DON'T** use fragile XPaths:
```python
# Avoid this - too specific
button = page.locator('//html/body/main/form/div[2]/button[1]')
```

### Waits and Timeouts

✅ **DO** use dynamic waits:
```python
await page.wait_for_selector(".success-message", state="visible")
await page.wait_for_load_state("networkidle")
```

❌ **DON'T** use fixed waits:
```python
# Avoid this
import time
time.sleep(5)
```

### Test Isolation

✅ **DO** create test-specific data:
```python
unique_email = f"user_{uuid.uuid4()}@example.com"
```

✅ **DO** clean up after tests:
```python
@pytest.fixture(autouse=True)
def cleanup():
    yield
    # Cleanup code here
```

### Assertions

✅ **DO** use meaningful assertions:
```python
assert url.endswith("/home"), "Not redirected to home page"
assert "Success" in message, "Success message not displayed"
```

❌ **DON'T** use trivial assertions:
```python
assert result  # Too vague
```

## CI/CD Integration

### GitHub Actions

The project includes GitHub Actions workflows for automated testing:

1. **Main Workflow** (`.github/workflows/tests.yml`):
   - Runs on push and pull requests
   - Tests on multiple OS and Python versions
   - Tests on multiple browsers
   - Generates Allure reports
   - Auto-deploys to GitHub Pages

2. **Scheduled Regression** (`.github/workflows/regression-tests.yml`):
   - Runs daily tests
   - Maintains test history
   - Generates trend reports

### Local CI simulation:

```bash
# Run as pre-commit hook
pytest tests/ --tb=short

# Run all quality checks
black .
flake8 tests/ pages/ utils/
mypy tests/ pages/ utils/ --ignore-missing-imports
```

## Reporting

### Allure Reports

Generate comprehensive HTML reports:

```bash
# Generate report
pytest tests/ --alluredir=allure-results
allure generate allure-results -o allure-report --clean

# View report locally
allure serve allure-results

# View generated report
open allure-report/index.html
```

### Test Report Features

- Test execution history
- Trend analysis
- Failed test categories
- Video/screenshot attachments
- Detailed test descriptions
- Environment information

## Troubleshooting

### Issue: Playwright browsers not installed

**Solution:**
```bash
playwright install
python -m playwright install-deps
```

### Issue: Tests timeout

**Solution:** Increase timeout in config:
```env
TIMEOUT=60000
NAVIGATION_TIMEOUT=60000
```

### Issue: Element not found

**Solution:**
1. Check selector using browser DevTools
2. Verify element is actually present (visible or hidden)
3. Add wait for element:
```python
await page.wait_for_selector(selector, timeout=10000)
```

### Issue: Test runs on CI but not locally

**Solution:**
1. Check environment variables
2. Clear browser cache: `rm -rf ~/.cache/ms-playwright`
3. Reinstall browsers: `playwright install`

## Performance Optimization

### Use parallel execution:
```bash
pip install pytest-xdist
pytest tests/ -n auto
```

### Use headless mode:
```env
HEADLESS=true
```

### Reduce slow motion:
```env
SLOW_MO=0
```

### Use smaller browser contexts:
```python
context = await browser.new_context(
    viewport={"width": 1280, "height": 720}
)
```

## Contributing

1. Create a feature branch
2. Write tests for new features
3. Ensure all tests pass
4. Submit pull request

## Resources

- [Playwright Python Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Allure Report Documentation](https://docs.qameta.io/allure/)
- [BookCart Application](https://bookcart.azurewebsites.net/)

## Support

For issues or questions:
1. Check this README
2. Review test examples in `tests/`
3. Check Playwright documentation
4. Review GitHub Issues

## License

This project is provided as-is for educational and testing purposes.
