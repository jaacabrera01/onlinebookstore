"""Debug script to check login and error messages."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def test_login():
    """Test login and show errors."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        # Navigate to login page
        await page.goto(f"{settings.BASE_URL}login")
        await page.wait_for_load_state("domcontentloaded")
        
        print(f"📍 Current URL: {page.url}")
        print(f"📝 Attempting login with:")
        print(f"   Username: {settings.TEST_USERNAME}")
        print(f"   Password: {settings.TEST_PASSWORD}")
        
        # Fill in credentials
        await page.fill('input[formcontrolname="username"]', settings.TEST_USERNAME)
        await page.fill('input[formcontrolname="password"]', settings.TEST_PASSWORD)
        
        # Click login
        await page.click('button:has-text("Login")')
        
        # Wait for response
        await page.wait_for_timeout(3000)
        
        print(f"\n📍 URL after login attempt: {page.url}")
        
        # Check for error messages
        error_selectors = [
            '.alert-danger',
            '.mat-error',
            '[role="alert"]',
            '.error-message',
            '.validation-error'
        ]
        
        for selector in error_selectors:
            errors = await page.locator(selector).all()
            if errors:
                print(f"\n❌ Found errors with selector '{selector}':")
                for error in errors:
                    text = await error.text_content()
                    if text.strip():
                        print(f"   - {text.strip()}")
        
        # Keep browser open for inspection
        await page.wait_for_timeout(10000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_login())
