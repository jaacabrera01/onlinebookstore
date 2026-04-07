"""Debug script to try different submit methods."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def test_submit_methods():
    """Test different ways to submit the registration form."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        password = "TestPass123!"
        
        # Navigate
        await page.goto(f"{settings.BASE_URL}register")
        await page.wait_for_load_state("networkidle")
        
        # Fill form
        await page.fill('input[formcontrolname="firstName"]', "Test")
        await page.fill('input[formcontrolname="lastName"]', "User")
        await page.fill('input[formcontrolname="userName"]', username)
        await page.fill('input[formcontrolname="password"]', password)
        await page.fill('input[formcontrolname="confirmPassword"]', password)
        
        # Try Method 1: Find button and get its exact selector
        print(f"\n🔍 Method 1: Inspect the Register button...")
        buttons = await page.query_selector_all("button")
        register_button = None
        for btn in buttons:
            text = await btn.text_content()
            if "Register" in text:
                register_button = btn
                print(f"   Found Register button with text: '{text.strip()}'")
                break
        
        if register_button:
            # Try clicking with force
            print(f"\n🔘 Method 1: Click with force=True...")
            await register_button.click(force=True)
            await page.wait_for_timeout(2000)
            print(f"   URL after click: {page.url}")
        
        # Try Method 2: Press Enter on password field
        print(f"\n🔘 Method 2: Press Enter on password field...")
        await page.press('input[formcontrolname="confirmPassword"]', "Enter")
        await page.wait_for_timeout(2000)
        print(f"   URL after Enter: {page.url}")
        
        # Try Method 3: Check for form element and submit it
        print(f"\n🔍 Method 3: Looking for form element...")
        forms = await page.query_selector_all("form")
        print(f"   Found {len(forms)} form(s)")
        if forms:
            for i, form in enumerate(forms):
                print(f"   Submitting form {i}...")
                await form.evaluate("form => form.submit()")
                await page.wait_for_timeout(2000)
                print(f"   URL after form.submit(): {page.url}")
                break
        
        await page.wait_for_timeout(2000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_submit_methods())
