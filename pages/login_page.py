"""Login page object."""
from pages import BasePage
from playwright.async_api import Page


class LoginPage(BasePage):
    """Login page object model."""
    
    # Selectors - Angular Material form controls
    USERNAME_INPUT = 'input[formcontrolname="username"]'
    PASSWORD_INPUT = 'input[formcontrolname="password"]'
    LOGIN_BUTTON = 'button:has-text("Login")'
    REGISTER_LINK = 'a:has-text("New Customer")'
    ERROR_MESSAGE = '.alert-danger, .mat-error'
    REMEMBER_ME_CHECKBOX = 'input[type="checkbox"]'
    FORGOT_PASSWORD_LINK = 'a:has-text("Forgot your password")'
    
    async def goto_login(self):
        """Navigate to login page."""
        await self.goto("login")
    
    async def enter_username(self, username: str):
        """Enter username."""
        await self.fill(self.USERNAME_INPUT, username)
    
    async def enter_password(self, password: str):
        """Enter password."""
        await self.fill(self.PASSWORD_INPUT, password)
    
    async def click_login(self):
        """Submit login form by clicking the correct Login button."""
        # There are multiple Login buttons on the page, we need the second one (the form submit button)
        login_buttons = await self.page.query_selector_all('button:has-text("Login")')
        if len(login_buttons) >= 2:
            # Click the form submit button (typically the second one)
            await login_buttons[1].click(force=True)
        elif login_buttons:
            # Fallback to first button if only one exists
            await login_buttons[0].click(force=True)
        else:
            # Last resort: try pressing Enter
            await self.page.press(self.PASSWORD_INPUT, "Enter")
    
    async def login(self, username: str, password: str):
        """Complete login flow."""
        await self.enter_username(username)
        await self.enter_password(password)
        # Wait a moment for Angular to process input changes before submitting
        await self.page.wait_for_timeout(300)
        await self.click_login()
        
        # Wait for navigation to complete
        await self.page.wait_for_load_state("networkidle")
    
    async def click_register_link(self):
        """Click register link."""
        await self.click(self.REGISTER_LINK)
    
    async def get_error_message(self) -> str:
        """Get error message."""
        return await self.get_text(self.ERROR_MESSAGE)
    
    async def is_error_displayed(self) -> bool:
        """Check if error message is displayed."""
        return await self.is_visible(self.ERROR_MESSAGE, timeout=5000)
    
    async def click_remember_me(self):
        """Click remember me checkbox."""
        await self.check_element(self.REMEMBER_ME_CHECKBOX)
    
    async def click_forgot_password(self):
        """Click forgot password link."""
        await self.click(self.FORGOT_PASSWORD_LINK)
