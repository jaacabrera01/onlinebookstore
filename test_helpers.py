"""Helper to register test accounts."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def register_test_user(username: str = None, password: str = "TestPass123!"):
    """Register a test user and return credentials."""
    if username is None:
        username = f"testuser_{uuid.uuid4().hex[:8]}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        # Navigate to register page
        await page.goto(f"{settings.BASE_URL}register")
        await page.wait_for_load_state("networkidle")
        
        print(f"\n📝 Registering test user:")
        print(f"   Username: {username}")
        print(f"   Password: {password}")
        
        # Wait for form elements to be ready
        await page.wait_for_selector('input[formcontrolname="firstName"]', timeout=10000)
        
        # Fill registration form using keyboard for better Angular compatibility
        print(f"✍️  Filling form fields...")
        
        # First name
        await page.click('input[formcontrolname="firstName"]')
        await page.keyboard.type("Test")
        print(f"   ✅ First name filled")
        
        # Last name
        await page.click('input[formcontrolname="lastName"]')
        await page.keyboard.type("User")
        print(f"   ✅ Last name filled")
        
        # Username  
        await page.click('input[formcontrolname="userName"]')
        await page.keyboard.type(username)
        print(f"   ✅ Username filled: {username}")
        
        # Password
        await page.click('input[formcontrolname="password"]')
        await page.keyboard.type(password)
        print(f"   ✅ Password filled")
        
        # Confirm password
        await page.click('input[formcontrolname="confirmPassword"]')
        await page.keyboard.type(password)
        print(f"   ✅ Confirm password filled")
        
        # Select gender (required field)
        print(f"🔘 Selecting gender...")
        await page.click('input[type="radio"][value="Male"]')
        print(f"   ✅ Gender selected")
        
        print(f"🔘 Clicking Register button...")
        # Click register button
        await page.click('button:has-text("Register")')
        print(f"   ✅ Register button clicked")
        
        # Wait for response
        print(f"⏳ Waiting for registration response...")
        await page.wait_for_timeout(3000)
        
        current_url = page.url
        print(f"   Current URL: {current_url}")
        
        # Check if we got redirected to login (success) or still on register (failure)
        if "login" in current_url.lower():
            print(f"✅ Registration successful - redirected to login page")
        else:
            # Check for error messages
            error_elements = await page.query_selector_all(".alert-danger, .mat-error")
            if error_elements:
                for elem in error_elements:
                    text = await elem.text_content()
                    print(f"   ⚠️ Error: {text.strip()}")
            else:
                print(f"   ⚠️ Registration may have failed, still on: {current_url}")
        
        await page.wait_for_timeout(1000)
        await browser.close()
        
        return {"username": username, "password": password}


if __name__ == "__main__":
    creds = asyncio.run(register_test_user())
    print(f"\n✅ Test credentials created:")
    print(f"   Username: {creds['username']}")
    print(f"   Password: {creds['password']}")
