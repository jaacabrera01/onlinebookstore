"""Debug script to properly fill and submit login form."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings
from test_helpers import register_test_user

settings = get_settings()


async def test_login_with_proper_fill():
    """Test login with proper input handling."""
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
        
        # Method 1: Try filling with type instead of fill
        print(f"\n✍️ Method 1: Fill with type() instead of fill()...")
        await page.click('input[formcontrolname="username"]')
        await page.keyboard.type(username)
        
        await page.click('input[formcontrolname="password"]')
        await page.keyboard.type(password)
        
        # Wait a moment for Angular to process changes
        await page.wait_for_timeout(1000)
        
        # Check form validity
        username_input = await page.query_selector('input[formcontrolname="username"]')
        password_input = await page.query_selector('input[formcontrolname="password"]')
        
        username_class = await username_input.get_attribute("class")
        password_class = await password_input.get_attribute("class")
        
        print(f"   Username class: {username_class}")
        print(f"   Password class: {password_class}")
        
        # Get all Login buttons and try the second one
        print(f"\n🔘 Trying Login buttons...")
        buttons = await page.query_selector_all('button:has-text("Login")')
        print(f"   Found {len(buttons)} Login buttons")
        
        for i, btn in enumerate(buttons):
            print(f"\n   Trying Login button {i+1}...")
            await btn.click(force=True)
            await page.wait_for_timeout(2000)
            
            current_url = page.url
            print(f"      URL: {current_url}")
            
            # Check for logout button
            logout = await page.query_selector('button:has-text("Logout"), a:has-text("Logout")')
            if logout:
                print(f"      ✅ Logout button found - LOGIN SUCCESSFUL!")
                break
            
            # Try the next button if this one didn't work
            if i < len(buttons) - 1:
                print(f"      Continuing to next button...")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_login_with_proper_fill())
