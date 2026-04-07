# Test Automation Best Practices & Guidelines

## Table of Contents

1. [Test Structure](#test-structure)
2. [Writing Tests](#writing-tests)
3. [Assertions](#assertions)
4. [Handling Waits](#handling-waits)
5. [Test Data](#test-data)
6. [Error Handling](#error-handling)
7. [Performance](#performance)
8. [Debugging](#debugging)
9. [Maintenance](#maintenance)

## Test Structure

### AAA Pattern (Arrange, Act, Assert)

Every test should follow the Arrange-Act-Assert pattern:

```python
@pytest.mark.critical
async def test_user_login(self, page: Page):
    """Test user can login with valid credentials."""
    # ARRANGE - Setup
    login_page = LoginPage(page)
    email = "user@example.com"
    password = "TestPassword123!"
    
    # ACT - Perform actions
    await login_page.goto_login()
    await login_page.login(email, password)
    
    # ASSERT - Verify results
    url = await login_page.get_url()
    assert "login" not in url.lower(), "Still on login page"
```

### Test Naming Convention

- Use descriptive names starting with `test_`
- Include the feature being tested
- Include the expected outcome

```python
# ✅ Good
async def test_user_can_add_book_to_cart(self, page):
    
async def test_error_displayed_for_invalid_email(self, page):

# ❌ Bad
async def test_1(self, page):
    
async def test_login(self, page):
```

### Test Categories

Use pytest markers to categorize tests:

```python
@pytest.mark.smoke      # Quick critical path tests (2-5 min)
@pytest.mark.critical   # High-priority functionality  
@pytest.mark.regression # Comprehensive testing (30+ min)
@pytest.mark.slow       # Long-running tests (skip in CI)
```

## Writing Tests

### Basic Test Template

```python
"""Module description."""
import pytest
import allure
from pages.page_object import PageObject
from playwright.async_api import Page


@allure.feature("Feature Name")
@allure.suite("Test Suite Name")
class TestFeatureName:
    """Test cases for feature."""
    
    @allure.title("What the test does")
    @allure.description("Why this test is important")
    @pytest.mark.critical
    async def test_descriptive_name(self, page: Page):
        """
        Detailed docstring explaining:
        1. What is being tested
        2. Expected behavior
        3. Key assertions
        """
        # Test implementation
```

### Test with Setup/Teardown

```python
@pytest.fixture
async def authenticated_user(page):
    """Fixture to provide authenticated session."""
    login_page = LoginPage(page)
    await login_page.goto_login()
    await login_page.login("user@example.com", "password")
    return page


async def test_user_profile(authenticated_user):
    """Test when user is already authenticated."""
    profile_page = ProfilePage(authenticated_user)
    # Test continues with authenticated state
```

### Parametrized Tests

```python
@pytest.mark.parametrize("email,password,expected_error", [
    ("", "password", "Email is required"),
    ("invalid-email", "password", "Invalid email format"),
    ("user@example.com", "", "Password is required"),
])
async def test_login_validation_errors(self, page, email, password, expected_error):
    """Test various login validation errors."""
    login_page = LoginPage(page)
    await login_page.goto_login()
    await login_page.login(email, password)
    
    error_msg = await login_page.get_error_message()
    assert expected_error in error_msg
```

## Assertions

### Meaningful Assertions

✅ **DO** - Clear, specific assertions:
```python
# Check URL
url = await page.url
assert "checkout" in url.lower(), "Not navigated to checkout page"

# Check visibility
assert await product_page.is_success_displayed(), "Success message not shown"

# Check text content
title = await product_page.get_product_title()
assert title == "Expected Title", f"Got '{title}' instead"

# Check count
books = await home_page.get_featured_books_count()
assert books > 0, "No books displayed on home page"

# Check attribute
href = await page.get_attribute('a.link', 'href')
assert href == "/expected-page", f"Link points to {href}"
```

❌ **DON'T** - Vague assertions:
```python
# Too vague
assert result
assert isinstance(data, dict)
assert True

# Multiple assertions in one line
assert url and title and total
```

### Page Object Assertions

```python
# Use page object methods for assertions
assert await page_obj.is_visible(selector), "Element not visible"
assert await page_obj.is_element_enabled(selector), "Element disabled"
assert await page_obj.is_element_checked(selector), "Checkbox unchecked"
```

### API Assertions

```python
from utils.api_client import assert_response, assert_response_contains

# Assert status code
assert_response(response, 200)

# Assert response contains key
assert_response_contains(response, "status")

# Assert key-value pair
assert_response_contains(response, "status", "success")
```

## Handling Waits

### ✅ DO - Dynamic Waits

```python
# Wait for element visibility
await page.wait_for_selector(".success-message", state="visible", timeout=10000)

# Wait for page load
await page.wait_for_load_state("networkidle")

# Wait for URL change
await page.wait_for_url("**/checkout")

# Wait for condition
await page.wait_for_function(
    "() => document.querySelectorAll('.items').length > 0"
)

# Page object method
await page_obj.wait_for_element(selector, timeout=10000)
```

### ❌ DON'T - Fixed Waits

```python
# NEVER use sleep for waiting
import time
time.sleep(5)  # ❌ Bad

# NEVER use arbitrary delays
await page.wait_for_timeout(3000)  # ❌ Bad unless debugging
```

### Best Wait Practices

```python
# Use context managers for waiting
async with page.expect_navigation():
    await page.click("a.link")

# Wait for API response
async with page.expect_response("**/api/products") as response_info:
    await page.click("button.search")
response = await response_info.value

# Wait with custom condition
await page.locator(".item").first.wait_for(state="visible")
```

## Test Data

### Use Unique Test Data

```python
import uuid

@pytest.mark.critical
async def test_register_user(self, page):
    # ✅ Good - unique email each test
    unique_email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    
    register_page = RegisterPage(page)
    await register_page.register_user(
        first_name="Test",
        last_name="User",
        email=unique_email,
        password="TestPass123!"
    )
```

### Data-Driven Tests

```python
test_cases = [
    {"title": "Book 1", "category": "Fiction"},
    {"title": "Book 2", "category": "Science"},
]

@pytest.mark.parametrize("book", test_cases)
async def test_search_by_title(self, page, book):
    home_page = HomePage(page)
    await home_page.goto_home()
    await home_page.search_for_book(book["title"])
    # Verify results
```

### Fixtures for Common Data

```python
@pytest.fixture
def test_user():
    """Provide test user data."""
    return {
        "email": f"user_{uuid.uuid4()}@example.com",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User"
    }

async def test_with_user_data(self, page, test_user):
    register_page = RegisterPage(page)
    await register_page.register_user(**test_user)
```

## Error Handling

### Handle Transient Failures

```python
import asyncio

@pytest.mark.critical
async def test_with_retry(self, page):
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            login_page = LoginPage(page)
            await login_page.goto_login()
            await login_page.login("user@example.com", "password")
            break  # Success
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                raise
            await asyncio.sleep(2)  # Brief wait before retry
```

### Graceful Degradation

```python
async def test_with_optional_feature(self, page):
    cart_page = CartPage(page)
    await cart_page.goto_cart()
    
    # Try coupon - not critical
    try:
        await cart_page.apply_coupon("DISCOUNT10")
    except Exception:
        # Coupon feature might not be available
        pytest.skip("Coupon feature not available")
    
    # Continue with main test
    total = await cart_page.get_total()
    assert total, "Total not calculated"
```

## Performance

### Optimize Test Execution

```python
# ✅ Parallel execution
pytest tests/ -n auto

# ✅ Use shared fixtures
@pytest.fixture(scope="session")
async def browser():
    # Reuse across tests
    pass

# ✅ Skip non-critical on CI
@pytest.mark.slow
async def test_visual_regression(self, page):
    pass

# Run with -m "not slow" on CI
```

### Avoid Common Performance Killers

```python
# ❌ Don't navigate unnecessarily
await page.goto(url)
# Use page_obj.goto() which reuses context

# ❌ Don't take screenshots unless needed
if failure:
    await page.screenshot()  # ✅ Good

# ❌ Don't use full page screenshots in loops
for item in items:
    # Don't: await page.screenshot()  # ✅ Screenshot once at end
    pass
```

## Debugging

### Enable Debugging Features

```python
# Pause execution for debugging
async def test_debug(self, page):
    page_obj = PageObject(page)
    await page_obj.perform_action()
    
    # Pause for interactive debugging
    await page.pause()
    
    # Continue execution
    assert result
```

### Detailed Logging

```python
import logging

logger = logging.getLogger(__name__)

async def test_with_logging(self, page):
    logger.info("Starting test")
    logger.debug(f"Current URL: {page.url}")
    
    page_obj = PageObject(page)
    
    try:
        await page_obj.perform_action()
        logger.info("Action completed successfully")
    except Exception as e:
        logger.error(f"Action failed: {str(e)}")
        raise
```

### Screenshot on Failure

```python
@pytest.fixture(autouse=True)
async def take_screenshot_on_failure(page, request):
    """Automatically take screenshot on test failure."""
    yield
    
    if request.node.rep_call.failed:
        screenshot_name = f"fail_{request.node.name}.png"
        await page.screenshot(path=f"test-results/{screenshot_name}")
        logger.error(f"Screenshot saved: {screenshot_name}")
```

## Maintenance

### Updating Selectors

When UI changes and selectors break:

```python
# Old broken selector
BUTTON = ".submit-btn"

# Updated selector
BUTTON = 'button:has-text("Submit")'

# Or use data-test-id if available
BUTTON = '[data-test-id="submit-button"]'
```

### Handling Flaky Tests

```python
# Mark flaky tests
@pytest.mark.flaky(reruns=3, reruns_delay=2)
async def test_sometimes_flaky(self, page):
    # This test will retry 3 times if it fails
    pass

# Or handle in test
for i in range(3):
    try:
        await page_obj.perform_action()
        break
    except AssertionError:
        if i < 2:
            await page.reload()
        else:
            raise
```

### Test Documentation

```python
async def test_critical_purchase_flow(self, page):
    """
    Test the complete purchase flow from product selection to checkout.
    
    Steps:
    1. User navigates to home page
    2. Searches for a specific book
    3. Selects the first result
    4. Adds to cart with quantity = 2
    5. Proceeds to checkout
    6. Enters billing and payment information
    7. Places order
    
    Expected Result:
    - Order confirmation page displayed
    - Order number visible
    - Success message shown
    
    Related Tests:
    - test_search_functionality
    - test_product_detail_display
    - test_shopping_cart_management
    """
```

## Summary

| Do | Don't |
|----|-------|
| Use descriptive test names | Use vague names |
| Follow AAA pattern | Mix setup with actions |
| Use meaningful assertions | Use generic assertions |
| Use dynamic waits | Use sleep/fixed waits |
| Handle test data uniquely | Reuse test data |
| Tag tests appropriately | Leave tests untagged |
| Use page objects | Write direct Playwright code |
| Write docstrings | Skip documentation |
| Debug interactively | Add print statements |
| Take screenshots on failure | Always take screenshots |

---

For more information, see [README.md](../README.md) and [Page Objects](../pages/README.md).
