"""Debug script to test registration flow."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def debug_registration():
    """Debug the registration flow step by step."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        password = "TestPass123!"
        
        # Navigate to register page
        print(f"\n📝 Step 1: Navigate to register page")
        await page.goto(f"{settings.BASE_URL}register")
        await page.wait_for_load_state("networkidle")
        print(f"   ✅ URL: {page.url}")
        
        # Fill form
        print(f"\n✍️ Step 2: Fill registration form")
        await page.fill('input[formcontrolname="firstName"]', "Test")
        print(f"   ✅ First name filled")
        await page.fill('input[formcontrolname="lastName"]', "User")
        print(f"   ✅ Last name filled")
        await page.fill('input[formcontrolname="userName"]', username)
        print(f"   ✅ Username filled: {username}")
        await page.fill('input[formcontrolname="password"]', password)
        print(f"   ✅ Password filled")
        await page.fill('input[formcontrolname="confirmPassword"]', password)
        print(f"   ✅ Confirm password filled")
        
        # Submit
        print(f"\n🔘 Step 3: Click Register button")
        await page.click('button:has-text("Register")')
        print(f"   ✅ Register button clicked")
        
        # Wait for response
        print(f"\n⏳ Step 4: Wait for registration response")
        await page.wait_for_timeout(3000)
        print(f"   Current URL: {page.url}")
        
        # Check for success message or error
        print(f"\n🔍 Step 5: Check for success/error messages")
        
        # Check for error messages
        error_elements = await page.query_selector_all(".alert-danger, .mat-error, .error")
        if error_elements:
            for elem in error_elements:
                text = await elem.text_content()
                print(f"   ⚠️ Error found: {text.strip()}")
        
        # Check for success message
        success_elements = await page.query_selector_all(".alert-success, .success")
        if success_elements:
            for elem in success_elements:
                text = await elem.text_content()
                print(f"   ✅ Success message: {text.strip()}")
        
        # Now try to login with the registered account
        print(f"\n🔐 Step 6: Navigate to login page and test credentials")
        await page.goto(f"{settings.BASE_URL}login")
        await page.wait_for_load_state("networkidle")
        print(f"   ✅ URL: {page.url}")
        
        # Login
        print(f"\n✍️ Step 7: Enter login credentials")
        await page.fill('input[formcontrolname="username"]', username)
        await page.fill('input[formcontrolname="password"]', password)
        print(f"   ✅ Credentials filled")
        
        print(f"\n🔘 Step 8: Click Login button")
        await page.click('button:has-text("Login")')
        print(f"   ✅ Login button clicked")
        
        # Wait for response
        print(f"\n⏳ Step 9: Wait for login response")
        await page.wait_for_timeout(3000)
        print(f"   Current URL: {page.url}")
        
        # Check for logout button
        print(f"\n🔍 Step 10: Check for logout button")
        try:
            await page.wait_for_selector('button:has-text("Logout"), a:has-text("Logout")', timeout=2000)
            print(f"   ✅ Logout button FOUND - Login successful!")
        except:
            print(f"   ❌ Logout button NOT found - Login failed")
            
            # Check for error messages
            error_elements = await page.query_selector_all(".alert-danger, .mat-error, .error")
            if error_elements:
                for elem in error_elements:
                    text = await elem.text_content()
                    print(f"      Error: {text.strip()}")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_registration())
