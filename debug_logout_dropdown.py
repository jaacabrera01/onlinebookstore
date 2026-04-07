"""Debug script to find logout in dropdown menu."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings
from test_helpers import register_test_user

settings = get_settings()


async def find_logout_in_dropdown():
    """Find logout button in profile dropdown."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        # Register and login
        print(f"\n📝 Registering and logging in...")
        creds = await register_test_user()
        
        # Login
        await page.goto(f"{settings.BASE_URL}login")
        await page.wait_for_load_state("networkidle")
        
        await page.click('input[formcontrolname="username"]')
        await page.keyboard.type(creds["username"])
        
        await page.click('input[formcontrolname="password"]')
        await page.keyboard.type(creds["password"])
        
        await page.wait_for_timeout(500)
        await page.press('input[formcontrolname="password"]', "Enter")
        await page.wait_for_load_state("networkidle")
        
        print(f"✅ Logged in. Current URL: {page.url}")
        
        # Click on the profile/account link to open dropdown
        print(f"\n🔍 Looking for profile menu...")
        profile_link = await page.query_selector('a:has-text("' + creds["username"] + '"), [class*="account"] a, [class*="profile"] a')
        
        if not profile_link:
            # Try more generic search
            all_links = await page.query_selector_all("a")
            for link in all_links:
                text = await link.text_content()
                if creds["username"] in text:
                    profile_link = link
                    print(f"Found profile link with text containing username")
                    break
        
        if profile_link:
            print(f"Found profile link, clicking...")
            await profile_link.click()
            await page.wait_for_timeout(1000)
            
            # Now look for logout button
            print(f"\n🔍 Looking for logout button in dropdown...")
            all_elements = await page.query_selector_all("button, a")
            
            for elem in all_elements:
                text = await elem.text_content()
                if text and ("logout" in text.lower() or "sign out" in text.lower() or "log out" in text.lower()):
                    print(f"   ✅ Found logout: {text.strip()}")
        else:
            # Look for any menu that might appear
            print(f"   Could not find profile link")
            
            # Try clicking on the account icon/button area
            print(f"\n   Trying to find account button...")
            account_elements = await page.query_selector_all("button[aria-label*='account'], [class*='account'] button, [class*='profile'] button")
            
            if account_elements:
                print(f"   Found {len(account_elements)} account buttons, clicking first...")
                await account_elements[0].click()
                await page.wait_for_timeout(1000)
                
                # Look again
                all_elements = await page.query_selector_all("button, a, [role='menuitem']")
                for elem in all_elements:
                    text = await elem.text_content()
                    if text and len(text.strip()) > 0 and len(text.strip()) < 50:
                        if "logout" in text.lower() or "sign out" in text.lower():
                            print(f"      ✅ Found: {text.strip()}")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(find_logout_in_dropdown())
