"""Debug script to try Enter key to submit."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings
from test_helpers import register_test_user

settings = get_settings()


async def test_login_with_enter_key():
    """Test login using Enter key instead of button click."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        # Register user
        print(f"\n📝 Registering test user...")
        creds = await register_test_user()
        username = creds["username"]
        password = creds["password"]
        
        # Navigate to login
        print(f"\n🔗 Navigating to login page...")
        await page.goto(f"{settings.BASE_URL}login")
        await page.wait_for_load_state("networkidle")
        
        # Fill form using keyboard
        print(f"\n✍️ Filling form with keyboard...")
        await page.click('input[formcontrolname="username"]')
        await page.keyboard.type(username)
        
        await page.click('input[formcontrolname="password"]')
        await page.keyboard.type(password)
        
        await page.wait_for_timeout(500)
        
        # Method 1: Press Enter on password field
        print(f"\n🔘 Method 1: Press Enter on password field...")
        await page.press('input[formcontrolname="password"]', "Enter")
        await page.wait_for_timeout(3000)
        
        current_url = page.url
        print(f"   URL after Enter: {current_url}")
        
        logout = await page.query_selector('button:has-text("Logout"), a:has-text("Logout")')
        if logout:
            print(f"   ✅ Logout button found - LOGIN SUCCESSFUL!")
            await page.wait_for_timeout(3000)
            await browser.close()
            return
        
        # Method 2: Try to evaluate JavaScript to click the button
        print(f"\n🔘 Method 2: Click Login button via JavaScript...")
        
        # Get all buttons that say "Login"
        login_buttons = await page.query_selector_all('button:has-text("Login")')
        
        for i, btn in enumerate(login_buttons):
            print(f"   Trying button {i+1} via JavaScript...")
            await page.evaluate("(btn) => btn.dispatchEvent(new MouseEvent('click', { bubbles: true }))", btn)
            await page.wait_for_timeout(2000)
            
            current_url = page.url
            print(f"      URL: {current_url}")
            
            logout = await page.query_selector('button:has-text("Logout"), a:has-text("Logout")')
            if logout:
                print(f"      ✅ Logout button found - LOGIN SUCCESSFUL!")
                await page.wait_for_timeout(3000)
                await browser.close()
                return
        
        # Method 3: Try to find and submit the form directly
        print(f"\n🔘 Method 3: Submit form via JavaScript...")
        forms = await page.query_selector_all("form")
        
        for i, form in enumerate(forms):
            print(f"   Trying form {i+1}...")
            # Try to get form's onsubmit or find a submit button within it
            form_inputs = await form.query_selector_all("input[formcontrolname]")
            print(f"      Form has {len(form_inputs)} form inputs")
            
            if len(form_inputs) >= 2:  # This is likely the login form
                # Try to submit via form.submit()
                await page.evaluate("(form) => form.submit()", form)
                await page.wait_for_timeout(2000)
                
                current_url = page.url
                print(f"      URL after form.submit(): {current_url}")
                
                logout = await page.query_selector('button:has-text("Logout"), a:has-text("Logout")')
                if logout:
                    print(f"      ✅ Logout button found - LOGIN SUCCESSFUL!")
                    await page.wait_for_timeout(3000)
                    await browser.close()
                    return
        
        print(f"\n❌ Login failed with all methods")
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_login_with_enter_key())
