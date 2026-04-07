"""Tests for user authentication (login and registration)."""
import pytest
import allure
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.home_page import HomePage
from playwright.async_api import Page
from config import get_settings
import uuid
from test_helpers import register_test_user

settings = get_settings()


@pytest.fixture(scope="session")
async def test_credentials():
    """Register and return test credentials for the session."""
    print("\n🔐 Setting up test credentials...")
    creds = await register_test_user()
    print(f"✅ Test account created: {creds['username']}")
    return creds


@allure.feature("Authentication")
@allure.suite("User Login")
class TestUserLogin:
    """Test cases for user login functionality."""
    
    @allure.title("User can login with valid credentials")
    @allure.description("Verify that a user can successfully login with valid email and password")
    @pytest.mark.critical
    @pytest.mark.smoke
    async def test_login_with_valid_credentials(self, page: Page):
        """Test successful login with valid credentials."""
        import uuid
        
        # First, register a new test user
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        password = "TestPass123!"
        
        print(f"\n📝 Registering test user: {username}")
        await page.goto(f"{settings.BASE_URL}register", wait_until="domcontentloaded")
        
        await page.fill('input[formcontrolname="firstName"]', "Test")
        await page.fill('input[formcontrolname="lastName"]', "User")
        await page.fill('input[formcontrolname="userName"]', username)
        await page.fill('input[formcontrolname="password"]', password)
        await page.fill('input[formcontrolname="confirmPassword"]', password)
        
        # Select gender (required)
        genders = await page.query_selector_all('input[type="radio"]')
        await genders[0].click()  # Click first radio (Male)
        
        # Click Register button (use last one)
        register_btns = await page.query_selector_all('button:has-text("Register")')
        await register_btns[-1].click()
        
        await page.wait_for_timeout(3000)
        
        assert "login" in page.url.lower(), f"Registration failed. URL: {page.url}"
        print(f"✅ Registration successful")
        
        # Now login  
        print(f"\n🔐 Logging in as: {username}")
        
        # Make sure we're on login page
        if "login" not in page.url.lower():
            await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
        
        # Use fill() method for login fields
        print(f"   Filling username...")
        await page.fill('input[formcontrolname="username"]', username)
        print(f"   Filling password...")
        await page.fill('input[formcontrolname="password"]', password)
        
        # Verify fields are filled
        username_val = await page.input_value('input[formcontrolname="username"]')
        password_val = await page.input_value('input[formcontrolname="password"]')
        print(f"   Username in form: {username_val}")
        print(f"   Password in form: {password_val}")
        
        await page.wait_for_timeout(1000)
        
        # Click the last Login button
        print(f"   Clicking Login button...")
        login_btns = await page.query_selector_all('button:has-text("Login")')
        print(f"   Found {len(login_btns)} Login buttons")
        assert len(login_btns) > 0, "No Login buttons found"
        await login_btns[-1].click()
        
        # Wait for redirect
        await page.wait_for_timeout(2000)
        
        # Verify successful redirect
        current_url = page.url
        print(f"   URL after login: {current_url}")
        
        # Check that we're NOT on the login page anymore
        assert "login" not in current_url.lower(), f"Still on login page after login. URL: {current_url}"
    
    @allure.title("User cannot login with invalid credentials")
    @allure.description("Verify that login fails with wrong credentials")
    @pytest.mark.critical
    async def test_login_with_invalid_password(self, page: Page):
        """Test login fails with invalid password."""
        login_page = LoginPage(page)
        
        await login_page.goto_login()
        
        # Try to login with invalid credentials
        await page.fill('input[formcontrolname="username"]', "invalid_user")
        await page.fill('input[formcontrolname="password"]', "WrongPassword123!")
        
        await page.wait_for_timeout(500)
        
        # Click login button
        login_btns = await page.query_selector_all('button:has-text("Login")')
        if login_btns:
            await login_btns[-1].click()
            await page.wait_for_timeout(2000)
        
        # Verify we're still on login page (login failed)
        assert "login" in page.url.lower(), "Should stay on login page after invalid credentials"
    
    @allure.title("User cannot login with non-existent email")
    @allure.description("Verify that login fails with non-existent user")
    @pytest.mark.critical
    async def test_login_with_nonexistent_account(self, page: Page):
        """Test login with non-existent account."""
        login_page = LoginPage(page)
        
        await login_page.goto_login()
        
        # Try to login with non-existent account
        await page.fill('input[formcontrolname="username"]', "nonexistent_user_xyz")
        await page.fill('input[formcontrolname="password"]', "TestPassword123!")
        
        await page.wait_for_timeout(500)
        
        # Click login button
        login_btns = await page.query_selector_all('button:has-text("Login")')
        if login_btns:
            await login_btns[-1].click()
            await page.wait_for_timeout(2000)
        
        # Verify we're still on login page (login failed)
        assert "login" in page.url.lower(), "Should stay on login page for non-existent account"
    
    @allure.title("Login page displays all required fields")
    @allure.description("Verify that login page has username, password, and submit button")
    @pytest.mark.regression
    async def test_login_page_layout(self, page: Page):
        """Test login page has all required elements."""
        login_page = LoginPage(page)
        
        await login_page.goto_login()
        
        # Check for username input
        assert await login_page.is_visible(LoginPage.USERNAME_INPUT), "Username input not visible"
        
        # Check for password input
        assert await login_page.is_visible(LoginPage.PASSWORD_INPUT), "Password input not visible"


@allure.feature("Authentication")
@allure.suite("User Registration")
class TestUserRegistration:
    """Test cases for user registration functionality."""
    
    @allure.title("User can register with valid details")
    @allure.description("Verify that a user can successfully register with valid information")
    @pytest.mark.critical
    @pytest.mark.smoke
    async def test_register_new_user(self, page: Page):
        """Test successful user registration."""
        register_page = RegisterPage(page)
        
        # Generate unique email
        unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
        
        await register_page.goto_register()
        
        # Register user
        await register_page.register_user(
            first_name="Test",
            last_name="User",
            email=unique_email,
            password="TestPassword123!",
            gender="Male"
        )
        
        # Verify redirect to login page after successful registration
        await page.wait_for_timeout(2000)
        current_url = page.url
        assert "login" in current_url.lower(), f"Expected redirect to login page, but got {current_url}"
    
    @allure.title("User cannot register with existing email")
    @allure.description("Verify that registration fails with already registered email")
    @pytest.mark.critical
    async def test_register_with_existing_email(self, page: Page):
        """Test registration fails with existing email."""
        register_page = RegisterPage(page)
        
        await register_page.goto_register()
        
        # Try to register with existing email
        await register_page.register_user(
            first_name="Test",
            last_name="User",
            email="testuser@example.com",
            password="TestPassword123!"
        )
        
        # Should show error
        is_error = await register_page.is_error_displayed()
        assert is_error, "No error displayed for existing email"
    
    @allure.title("Password fields must match")
    @allure.description("Verify that registration fails when passwords don't match")
    @pytest.mark.critical
    async def test_register_password_mismatch(self, page: Page):
        """Test registration with mismatched passwords."""
        register_page = RegisterPage(page)
        
        unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
        
        await register_page.goto_register()
        await register_page.enter_first_name("Test")
        await register_page.enter_last_name("User")
        await register_page.enter_email(unique_email)
        await register_page.enter_password("TestPassword123!")
        await register_page.enter_confirm_password("DifferentPassword123!")
        await register_page.accept_terms()
        await register_page.click_register()
        
        # Should show error
        is_error = await register_page.is_error_displayed()
        assert is_error, "No error for password mismatch"
    
    @allure.title("Registration page displays all required fields")
    @allure.description("Verify registration form has all required input fields")
    @pytest.mark.regression
    async def test_registration_page_layout(self, page: Page):
        """Test registration page has all required fields."""
        register_page = RegisterPage(page)
        
        await register_page.goto_register()
        
        assert await register_page.is_visible(RegisterPage.FIRST_NAME_INPUT), \
            "First name input not visible"
        assert await register_page.is_visible(RegisterPage.LAST_NAME_INPUT), \
            "Last name input not visible"
        assert await register_page.is_visible(RegisterPage.EMAIL_INPUT), \
            "Email input not visible"
        assert await register_page.is_visible(RegisterPage.PASSWORD_INPUT), \
            "Password input not visible"
        assert await register_page.is_visible(RegisterPage.REGISTER_BUTTON), \
            "Register button not visible"


@allure.feature("Authentication")
@allure.suite("Navigation")
class TestAuthenticationNavigation:
    """Test authentication navigation between pages."""
    
    @allure.title("User can navigate from login to registration")
    @allure.description("Verify navigation from login page to registration page")
    @pytest.mark.regression
    async def test_navigate_login_to_register(self, page: Page):
        """Test navigation from login to register page."""
        login_page = LoginPage(page)
        
        await login_page.goto_login()
        await login_page.click_register_link()
        
        # Verify on registration page
        url = await login_page.get_url()
        assert "register" in url.lower(), "Not navigated to registration page"
    
    @allure.title("User can navigate from registration to login")
    @allure.description("Verify navigation from registration page to login page")
    @pytest.mark.regression
    async def test_navigate_register_to_login(self, page: Page):
        """Test navigation from register to login page."""
        register_page = RegisterPage(page)
        
        await register_page.goto_register()
        await register_page.click_login_link()
        
        # Verify on login page
        url = await register_page.get_url()
        assert "login" in url.lower(), "Not navigated to login page"
