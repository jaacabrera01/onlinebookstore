"""Debug script to find the logout button."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings
from test_helpers import register_test_user

settings = get_settings()


async def find_logout_button():
    """Find the logout button on the home page."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        # Register and login
        print(f"\n📝 Registering test user...")
        creds = await register_test_user()
        
        # Navigate to login
        print(f"\n🔗 Navigating to login page...")
        await page.goto(f"{settings.BASE_URL}login")
        await page.wait_for_load_state("networkidle")
        
        # Login using keyboard
        await page.click('input[formcontrolname="username"]')
        await page.keyboard.type(creds["username"])
        
        await page.click('input[formcontrolname="password"]')
        await page.keyboard.type(creds["password"])
        
        await page.wait_for_timeout(500)
        await page.press('input[formcontrolname="password"]', "Enter")
        await page.wait_for_load_state("networkidle")
        
        print(f"\n✅ Logged in. Current URL: {page.url}")
        
        # Find logout button in navbar
        print(f"\n🔍 Looking for logout button...")
        
        # Check all buttons
        buttons = await page.query_selector_all("button, a")
        print(f"\n📋 All buttons/links:")
        for i, btn in enumerate(buttons[:20]):
            text = await btn.text_content()
            tag = await btn.evaluate("el => el.tagName")
            aria_label = await btn.get_attribute("aria-label")
            
            text_clean = text.strip() if text else ""
            
            # Look for logout-related text
            if "logout" in text_clean.lower() or "sign out" in text_clean.lower() or "log out" in text_clean.lower():
                print(f"   {i+1}. <{tag}> text='{text_clean}' aria-label={aria_label}")
            elif i < 10:  # Show first 10 anyway
                print(f"   {i+1}. <{tag}> text='{text_clean}' aria-label={aria_label}")
        
        # Try to find by checking the navbar/profile area
        print(f"\n🔍 Checking navbar area...")
        navbar = await page.query_selector("nav, [role='navigation'], .navbar, .header")
        if navbar:
            navbar_buttons = await navbar.query_selector_all("button, a")
            print(f"   Found {len(navbar_buttons)} buttons/links in navbar")
            for btn in navbar_buttons:
                text = await btn.text_content()
                if text and len(text.strip()) > 0 and len(text.strip()) < 50:
                    print(f"      - {text.strip()}")
        
        # Look for profile dropdown or menu
        print(f"\n🔍 Looking for profile/account menu...")
        profile = await page.query_selector("[class*='profile'], [class*='account'], [class*='user'], [class*='menu']")
        if profile:
            profile_buttons = await profile.query_selector_all("button, a")
            for btn in profile_buttons:
                text = await btn.text_content()
                if text:
                    print(f"   Found in profile: {text.strip()}")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(find_logout_button())
