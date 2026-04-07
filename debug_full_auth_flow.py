"""Debug script to check login form validation."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings
from test_helpers import register_test_user

settings = get_settings()


async def debug_login():
    """Debug the login process."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        # First, register a test user
        print(f"\n📝 Step 1: Register a test user...")
        creds = await register_test_user()
        username = creds["username"]
        password = creds["password"]
        print(f"✅ User registered: {username}")
        
        # Now go to login page (should already be there after registration)
        print(f"\n🔗 Step 2: Navigate to login page...")
        await page.goto(f"{settings.BASE_URL}login")
        await page.wait_for_load_state("networkidle")
        print(f"✅ URL: {page.url}")
        
        # Check form fields
        print(f"\n🔍 Step 3: Check login form fields...")
        username_input = await page.query_selector('input[formcontrolname="username"]')
        password_input = await page.query_selector('input[formcontrolname="password"]')
        login_button = await page.query_selector('button:has-text("Login")')
        
        print(f"   Username input: {username_input is not None}")
        print(f"   Password input: {password_input is not None}")
        print(f"   Login button: {login_button is not None}")
        
        # Fill the login form
        print(f"\n✍️ Step 4: Fill login form...")
        await page.fill('input[formcontrolname="username"]', username)
        await page.fill('input[formcontrolname="password"]', password)
        print(f"✅ Credentials filled: {username} / {password}")
        
        # Check for validation errors before submit
        print(f"\n🔍 Step 5: Check for validation errors BEFORE submit...")
        inputs = await page.query_selector_all("input")
        for inp in inputs:
            formcontrol = await inp.get_attribute("formcontrolname")
            aria_invalid = await inp.get_attribute("aria-invalid")
            if formcontrol and (aria_invalid or await inp.get_attribute("class") and "error" in await inp.get_attribute("class")):
                print(f"   ⚠️ {formcontrol}: aria-invalid={aria_invalid}")
        
        # Click login button
        print(f"\n🔘 Step 6: Click Login button...")
        await page.click('button:has-text("Login")')
        print(f"✅ Login button clicked")
        
        # Wait for response with longer timeout
        print(f"\n⏳ Step 7: Wait for login response (5 seconds)...")
        for i in range(5):
            await page.wait_for_timeout(1000)
            current_url = page.url
            print(f"   {i+1}s: {current_url}")
        
        # Check for error messages
        print(f"\n🔍 Step 8: Check for error messages...")
        error_elements = await page.query_selector_all(".alert-danger, .mat-error, .error")
        if error_elements:
            for elem in error_elements:
                text = await elem.text_content()
                visible = await elem.is_visible()
                if visible:
                    print(f"   ❌ Error (visible): {text.strip()}")
        else:
            print(f"   No error elements found")
        
        # Check for logout button
        print(f"\n🔍 Step 9: Check for logout button...")
        logout_btn = await page.query_selector('button:has-text("Logout"), a:has-text("Logout")')
        if logout_btn:
            print(f"   ✅ Found logout button - LOGIN SUCCESSFUL!")
        else:
            print(f"   ❌ Logout button not found - LOGIN FAILED")
        
        # Check page content
        print(f"\n📄 Step 10: Check page title and content...")
        title = await page.title()
        print(f"   Title: {title}")
        
        body_text = await page.text_content("body")
        if "dashboard" in body_text.lower() or "home" in body_text.lower():
            print(f"   ✅ Page indicates logged in")
        if "login" in body_text.lower():
            print(f"   ❌ Page still shows login form")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_login())
