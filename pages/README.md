# Page Object Models Documentation

## Overview

This directory contains Page Object Models (POM) that encapsulate the interactions with different pages of the BookCart application. Each page object provides methods to interact with UI elements without exposing implementation details to test code.

## Base Page Class

### `BasePage`
The base class that all page objects inherit from. Provides common functionality for all pages.

**Common Methods:**
- `goto(endpoint)` - Navigate to a specific page
- `is_visible(selector)` - Check if element is visible
- `wait_for_element(selector)` - Wait for element to appear
- `click(selector)` - Click an element
- `fill(selector, text)` - Fill an input field
- `get_text(selector)` - Get element text content
- `get_attribute(selector, attribute)` - Get element attribute
- `press_key(selector, key)` - Press a key
- `select_option(selector, value)` - Select dropdown option
- `get_url()` - Get current page URL
- `take_screenshot(name)` - Take screenshot
- `get_page_title()` - Get page title

**Example Usage:**
```python
from pages import BasePage

class MyPage(BasePage):
    BUTTON = "button.submit"
    
    async def click_submit(self):
        await self.click(self.BUTTON)
```

## Page Objects

### 1. HomePage (`home_page.py`)

Main landing page with search functionality and product browsing.

**Key Methods:**
- `goto_home()` - Navigate to home page
- `search_for_book(query)` - Search for books
- `select_category(category)` - Filter by category
- `click_book_by_title(title)` - Click a book
- `open_cart()` - Open shopping cart
- `click_login()` / `click_logout()` - Authentication
- `get_featured_books_count()` - Get visible books
- `is_user_logged_in()` - Check login status

**Example:**
```python
home_page = HomePage(page)
await home_page.goto_home()
await home_page.search_for_book("Python")
books_count = await home_page.get_featured_books_count()
```

### 2. LoginPage (`login_page.py`)

User login page with email/password fields.

**Key Methods:**
- `goto_login()` - Navigate to login page
- `enter_email(email)` - Enter email
- `enter_password(password)` - Enter password
- `click_login()` - Submit login form
- `login(email, password)` - Complete login flow
- `click_register_link()` - Navigate to registration
- `get_error_message()` - Get error text
- `is_error_displayed()` - Check for errors

**Example:**
```python
login_page = LoginPage(page)
await login_page.goto_login()
await login_page.login("user@example.com", "password")
```

### 3. RegisterPage (`register_page.py`)

User registration page with form fields.

**Key Methods:**
- `goto_register()` - Navigate to registration
- `register_user(first_name, last_name, email, password)` - Complete registration
- `enter_first_name(name)` - Enter first name
- `enter_last_name(name)` - Enter last name
- `enter_email(email)` - Enter email
- `enter_password(password)` - Enter password
- `enter_confirm_password(password)` - Confirm password
- `accept_terms()` - Accept terms checkbox
- `is_success_displayed()` - Check success message

**Example:**
```python
register_page = RegisterPage(page)
await register_page.goto_register()
await register_page.register_user("John", "Doe", "john@example.com", "Pass123!")
```

### 4. ProductDetailPage (`product_detail_page.py`)

Product details page with pricing, reviews, and add-to-cart.

**Key Methods:**
- `goto_product(product_id)` - Navigate to product
- `get_product_title()` - Get product title
- `get_product_price()` - Get product price
- `get_product_rating()` - Get rating
- `get_product_description()` - Get description
- `set_quantity(quantity)` - Set product quantity
- `add_to_cart(quantity)` - Add to cart
- `click_add_to_wishlist()` - Add to wishlist
- `get_related_products_count()` - Get related items

**Example:**
```python
product_page = ProductDetailPage(page)
await product_page.goto_product("book-123")
price = await product_page.get_product_price()
await product_page.add_to_cart(quantity=2)
```

### 5. CartPage (`cart_page.py`)

Shopping cart page with item management.

**Key Methods:**
- `goto_cart()` - Navigate to cart
- `get_cart_items_count()` - Get number of items
- `get_item_titles()` - Get all item names
- `update_item_quantity(index, quantity)` - Change item quantity
- `remove_item_from_cart(index)` - Remove item
- `get_subtotal()` - Get subtotal
- `get_tax()` - Get tax amount
- `get_total()` - Get cart total
- `click_checkout()` - Proceed to checkout
- `apply_coupon(code)` - Apply coupon code
- `is_cart_empty()` - Check if empty

**Example:**
```python
cart_page = CartPage(page)
await cart_page.goto_cart()
await cart_page.update_item_quantity(0, 2)
await cart_page.click_checkout()
```

### 6. CheckoutPage (`checkout_page.py`)

Checkout page with address and payment forms.

**Key Methods:**
- `goto_checkout()` - Navigate to checkout
- `fill_billing_address(...)` - Fill address form
- `select_shipping_method(method)` - Select shipping
- `fill_credit_card(...)` - Enter card details
- `complete_checkout(...)` - Complete full checkout
- `click_place_order()` - Place order
- `is_order_confirmation_displayed()` - Check confirmation
- `get_order_number()` - Get order ID
- `get_success_message()` - Get success text

**Example:**
```python
checkout_page = CheckoutPage(page)
await checkout_page.goto_checkout()
await checkout_page.fill_billing_address(
    first_name="John",
    last_name="Doe",
    email="john@example.com",
    phone="5551234567",
    address="123 Main St",
    city="New York",
    state="NY",
    zip_code="10001"
)
await checkout_page.fill_credit_card("4111111111111111", "12/26", "123", "John Doe")
await checkout_page.click_place_order()
```

## Selector Strategy

### Best Practices

1. **Data Test IDs** (Preferred)
   ```python
   BUTTON = '[data-test-id="login-button"]'
   ```

2. **User-Facing Text**
   ```python
   BUTTON = 'button:has-text("Sign In")'
   ```

3. **Type and Attributes**
   ```python
   EMAIL = 'input[type="email"]'
   ```

4. **Placeholders**
   ```python
   SEARCH = 'input[placeholder="Search Books"]'
   ```

### Avoid:
- Long XPath expressions
- Complex CSS selectors
- Classes that might change
- Index-based selectors

## Creating New Page Objects

### 1. Create a new file:
```python
# pages/my_page.py
from pages import BasePage

class MyPage(BasePage):
    """Page object for my page."""
    
    # Define selectors as class variables
    TITLE = "h1.page-title"
    BUTTON = 'button:has-text("Submit")'
    INPUT_FIELD = 'input[name="field-name"]'
    
    async def goto_my_page(self):
        """Navigate to my page."""
        await self.goto("my-page")
    
    async def perform_action(self):
        """Perform an action."""
        await self.click(self.BUTTON)
```

### 2. Use in tests:
```python
from pages.my_page import MyPage

async def test_my_feature(self, page):
    my_page = MyPage(page)
    await my_page.goto_my_page()
    await my_page.perform_action()
    assert await my_page.is_visible(my_page.TITLE)
```

## Common Patterns

### Waiting for Elements
```python
# Wait for element to be visible
await self.wait_for_element(self.SUCCESS_MESSAGE, timeout=5000)

# Check if element is visible
if await self.is_visible(self.BUTTON):
    await self.click(self.BUTTON)
```

### Form Filling
```python
async def fill_form(self, **kwargs):
    await self.fill(self.FIRST_NAME, kwargs.get('first_name', ''))
    await self.fill(self.LAST_NAME, kwargs.get('last_name', ''))
    await self.fill(self.EMAIL, kwargs.get('email', ''))
```

### Navigation with Wait
```python
async def navigate_and_wait(self, endpoint):
    await self.goto(endpoint)
    await self.page.wait_for_load_state("networkidle")
```

### Extracting Data
```python
async def get_all_items(self):
    """Get all item titles from page."""
    elements = self.page.locator(self.ITEM_SELECTOR)
    count = await elements.count()
    return [await elements.nth(i).text_content() for i in range(count)]
```

## Debugging Page Objects

### Enable Debug Output
```python
await page.pause()  # Pause execution for debugging
```

### Inspect Elements
```python
# Get element count
count = await page.locator(selector).count()

# Get element visibility
is_visible = await page.locator(selector).is_visible()

# Get element text
text = await page.locator(selector).text_content()
```

### Take Screenshots
```python
await self.take_screenshot("debug-screenshot")
```

## Best Practices

1. ✅ Keep selectors simple and maintainable
2. ✅ Use descriptive method names
3. ✅ Add docstrings to methods
4. ✅ Return meaningful data
5. ✅ Handle waits properly
6. ✅ Use consistent naming conventions
7. ✅ Group related methods together

## Resources

- [Playwright Python Docs](https://playwright.dev/python/)
- [Page Object Model Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [Test Automation Best Practices](https://www.testim.io/blog/page-object-model/)
