"""Debug script with extended debugging."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def test_with_debugging():
    """Test with extended debugging and longer waits."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        password = "TestPass123!"
        
        # REGISTER
        print(f"\n📝 Registering: {username}")
        await page.goto(f"{settings.BASE_URL}register")
        await page.wait_for_load_state("networkidle")
        
        await page.click('input[formcontrolname="firstName"]')
        await page.keyboard.type("Test")
        await page.click('input[formcontrolname="lastName"]')
        await page.keyboard.type("User")
        await page.click('input[formcontrolname="userName"]')
        await page.keyboard.type(username)
        await page.click('input[formcontrolname="password"]')
        await page.keyboard.type(password)
        await page.click('input[formcontrolname="confirmPassword"]')
        await page.keyboard.type(password)
        await page.click('input[type="radio"][value="Male"]')
        await page.click('button:has-text("Register")')
        
        await page.wait_for_timeout(3000)  # Longer wait
        print(f"✅ After registration. URL: {page.url}")
        
        # Check if there are error messages
        errors = await page.query_selector_all(".alert-danger, .mat-error, [role='alert']")
        if errors:
            for err in errors:
                text = await err.text_content()
                visible = await err.is_visible()
                if visible:
                    print(f"   Error: {text.strip()}")
        
        # LOGIN with longer waits
        print(f"\n🔐 Logging in...")
        
        # Wait for inputs to be ready
        await page.wait_for_selector('input[formcontrolname="username"]', timeout=10000)
        
        # Fill inputs
        await page.click('input[formcontrolname="username"]')
        await page.keyboard.type(username)
        await page.click('input[formcontrolname="password"]')
        await page.keyboard.type(password)
        
        # Wait longer for form validation
        print(f"   Waiting 2 seconds for form validation...")
        await page.wait_for_timeout(2000)
        
        # Check form inputs
        username_val = await page.input_value('input[formcontrolname="username"]')
        password_val = await page.input_value('input[formcontrolname="password"]')
        print(f"   Username value: {username_val}")
        print(f"   Password value: {password_val}")
        
        # Check all Login buttons and their states
        login_buttons = await page.query_selector_all('button:has-text("Login")')
        print(f"\n   Found {len(login_buttons)} Login buttons:")
        for i, btn in enumerate(login_buttons):
            disabled = await btn.is_disabled()
            classes = await btn.get_attribute("class")
            aria_label = await btn.get_attribute("aria-label")
            print(f"   Button {i+1}: disabled={disabled}, aria-label={aria_label}")
        
        # Try clicking
        print(f"\n   Clicking button 2...")
        if len(login_buttons) >= 2:
            await login_buttons[1].click(force=True)
            print(f"   Clicked, waiting 3 seconds...")
            await page.wait_for_timeout(3000)
            print(f"   URL: {page.url}")
            
            # Check for errors
            errors = await page.query_selector_all(".alert-danger, .mat-error, [role='alert']")
            if errors:
                for err in errors:
                    text = await err.text_content()
                    visible = await err.is_visible()
                    if visible:
                        print(f"   Login error: {text.strip()}")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_with_debugging())
