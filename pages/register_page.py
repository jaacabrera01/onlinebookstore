"""User registration page object."""
from pages import BasePage


class RegisterPage(BasePage):
    """User registration page object model."""
    
    # Selectors
    FIRST_NAME_INPUT = 'input[formcontrolname="firstName"]'
    LAST_NAME_INPUT = 'input[formcontrolname="lastName"]'
    USERNAME_INPUT = 'input[formcontrolname="userName"]'
    PASSWORD_INPUT = 'input[formcontrolname="password"]'
    CONFIRM_PASSWORD_INPUT = 'input[formcontrolname="confirmPassword"]'
    GENDER_SELECT = 'input[formcontrolname="gender"], select[formcontrolname="gender"], mat-select[formcontrolname="gender"]'
    REGISTER_BUTTON = 'button:has-text("Register")'
    LOGIN_LINK = 'a:has-text("Existing Customer")'
    
    async def goto_register(self):
        """Navigate to register page."""
        await self.goto("register")
    
    async def enter_first_name(self, first_name: str):
        """Enter first name."""
        await self.fill(self.FIRST_NAME_INPUT, first_name)
    
    async def enter_last_name(self, last_name: str):
        """Enter last name."""
        await self.fill(self.LAST_NAME_INPUT, last_name)
    
    async def enter_email(self, email: str):
        """Enter email (alias for username field in this form)."""
        await self.fill(self.USERNAME_INPUT, email)
    
    async def enter_password(self, password: str):
        """Enter password."""
        await self.fill(self.PASSWORD_INPUT, password)
    
    async def enter_confirm_password(self, password: str):
        """Enter confirm password."""
        await self.fill(self.CONFIRM_PASSWORD_INPUT, password)
    
    async def select_gender(self, gender: str = "Male"):
        """Select gender from radio buttons or dropdown."""
        # Try radio buttons first
        genders = await self.page.query_selector_all('input[type="radio"]')
        if genders and len(genders) > 0:
            if gender.lower() == "male" and len(genders) > 0:
                await genders[0].click()
            elif gender.lower() == "female" and len(genders) > 1:
                await genders[1].click()
        else:
            # Try select element
            try:
                await self.select_option(self.GENDER_SELECT, gender)
            except:
                # Try filling if it's a text input
                await self.fill(self.GENDER_SELECT, gender)
    
    async def click_register(self):
        """Click register button."""
        await self.click(self.REGISTER_BUTTON)
    
    async def register_user(self, first_name: str, last_name: str, email: str, password: str, gender: str = "Male"):
        """Complete registration flow."""
        await self.enter_first_name(first_name)
        await self.enter_last_name(last_name)
        await self.enter_email(email)
        await self.enter_password(password)
        await self.enter_confirm_password(password)
        await self.select_gender(gender)
        await self.click_register()
        
        # Wait for response
        await self.page.wait_for_load_state("networkidle")
