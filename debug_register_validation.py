"""Debug script to check registration form validation."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def debug_registration_validation():
    """Debug registration form validation."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()
        
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        password = "TestPass123!"
        
        # Navigate to register page
        await page.goto(f"{settings.BASE_URL}register")
        await page.wait_for_load_state("networkidle")
        print(f"\n📄 Checking register page...")
        
        # Fill form
        await page.fill('input[formcontrolname="firstName"]', "Test")
        await page.fill('input[formcontrolname="lastName"]', "User")
        await page.fill('input[formcontrolname="userName"]', username)
        await page.fill('input[formcontrolname="password"]', password)
        await page.fill('input[formcontrolname="confirmPassword"]', password)
        
        print(f"✅ Form filled")
        
        # Check all form fields for errors
        print(f"\n🔍 Checking for validation errors:")
        all_inputs = await page.query_selector_all("input")
        for inp in all_inputs:
            cls = await inp.get_attribute("class")
            aria_invalid = await inp.get_attribute("aria-invalid")
            if aria_invalid or (cls and "error" in cls):
                fc = await inp.get_attribute("formcontrolname")
                print(f"   ⚠️ {fc}: aria-invalid={aria_invalid}, class={cls}")
        
        # Check if Register button is enabled
        print(f"\n🔘 Checking Register button:")
        register_btn = await page.query_selector('button:has-text("Register")')
        if register_btn:
            disabled = await register_btn.is_disabled()
            cls = await register_btn.get_attribute("class")
            print(f"   Disabled: {disabled}")
            print(f"   Class: {cls}")
        
        # Check for mat-error messages
        print(f"\n📋 Checking for error messages:")
        errors = await page.query_selector_all(".mat-error")
        if errors:
            for i, err in enumerate(errors):
                text = await err.text_content()
                visible = await err.is_visible()
                print(f"   Error {i+1} (visible={visible}): {text.strip()}")
        else:
            print(f"   No error elements found")
        
        # Try clicking the button and wait longer
        print(f"\n🔘 Attempting to click Register button...")
        await page.click('button:has-text("Register")')
        
        # Wait for page change or error
        print(f"⏳ Waiting 5 seconds for response...")
        for i in range(5):
            await page.wait_for_timeout(1000)
            current_url = page.url
            print(f"   {i+1}s: {current_url}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_registration_validation())
