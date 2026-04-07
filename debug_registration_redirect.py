"""Check registration redirect."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def check_registration_redirect():
    """Check where we end up after registration."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        password = "TestPass123!"
        
        print(f"📝 Starting at: {page.url}")
        await page.goto(f"{settings.BASE_URL}register", wait_until="networkidle")
        print(f"✅ At register page: {page.url}")
        
        # Fill form
        await page.fill('input[formcontrolname="firstName"]', "Test")
        await page.fill('input[formcontrolname="lastName"]', "User")
        await page.fill('input[formcontrolname="userName"]', username)
        await page.fill('input[formcontrolname="password"]', password)
        await page.fill('input[formcontrolname="confirmPassword"]', password)
        
        # Select gender
        genders = await page.query_selector_all('input[type="radio"]')
        await genders[0].click()
        
        # Click register button
        register_btns = await page.query_selector_all('button:has-text("Register")')
        print(f"📝 Found {len(register_btns)} Register buttons")
        
        # Monitor for navigation
        async def log_navigation():
            async def handler(page_): print(f"   Navigation: {page_.url}")
            page.on("framenavigated", handler)
        
        await log_navigation()
        
        print(f"📝 Clicking register button...")
        await register_btns[-1].click()
        
        # Wait for navigation
        await page.wait_for_load_state("networkidle", timeout=5000)
        print(f"📝 After click, URL: {page.url}")
        
        await page.wait_for_timeout(2000)
        print(f"✅ Final URL: {page.url}")
        
        # Check what buttons exist
        buttons = await page.query_selector_all('button')
        for btn in buttons:
            text = await btn.text_content()
            if text.strip():
                print(f"   Button: {text.strip()}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_registration_redirect())
