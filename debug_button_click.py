"""Debug button clicking in test context."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def debug_buttons():
    """Debug button clicking."""
    async with async_playwright() as p:
        # Use headless=False to see what's happening
        browser = await p.chromium.launch(headless=True, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()
        
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        password = "TestPass123!"
        
        # REGISTER
        print(f"\n📝 Registering: {username}")
        await page.goto(f"{settings.BASE_URL}register", wait_until="networkidle")
        
        await page.fill('input[formcontrolname="firstName"]', "Test")
        await page.fill('input[formcontrolname="lastName"]', "User")
        await page.fill('input[formcontrolname="userName"]', username)
        await page.fill('input[formcontrolname="password"]', password)
        await page.fill('input[formcontrolname="confirmPassword"]', password)
        
        # Gender
        genders = await page.query_selector_all('input[type="radio"]')
        await genders[0].click()
        
        # Register button
        register_btns = await page.query_selector_all('button:has-text("Register")')
        await register_btns[-1].click()
        
        await page.wait_for_timeout(3000)
        print(f"✅ Registered. URL: {page.url}")
        
        # LOGIN
        print(f"\n🔐 Login inspection...")
        await page.fill('input[formcontrolname="username"]', username)
        await page.fill('input[formcontrolname="password"]', password)
        await page.wait_for_timeout(500)
        
        # Inspect buttons
        login_btns = await page.query_selector_all('button:has-text("Login")')
        print(f"Found {len(login_btns)} Login buttons")
        
        for i, btn in enumerate(login_btns):
            # Get button text
            text = await btn.text_content()
            # Get button classes
            classes = await btn.get_attribute("class")
            # Get button attributes
            is_disabled = await btn.get_attribute("disabled")
            aria_disabled = await btn.get_attribute("aria-disabled")
            ng_disabled = await btn.get_attribute("ng-disabled")
            
            print(f"\n  Button {i}:")
            print(f"    Text: {text}")
            print(f"    Classes: {classes}")
            print(f"    Disabled attr: {is_disabled}")
            print(f"    Aria-disabled: {aria_disabled}")
            print(f"    NG-disabled: {ng_disabled}")
            
            # Check visibility
            is_visible = await btn.is_visible()
            is_enabled = await btn.is_enabled()
            print(f"    Visible: {is_visible}")
            print(f"    Enabled: {is_enabled}")
        
        # Try clicking last button
        print(f"\n✅ Attempting to click last button...")
        try:
            await login_btns[-1].click(timeout=5000)
            await page.wait_for_timeout(2000)
            print(f"   SUCCESS - URL: {page.url}")
        except Exception as e:
            print(f"   FAILED - {e}")
            print(f"   Current URL: {page.url}")
        
        await context.close()
        await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_buttons())
