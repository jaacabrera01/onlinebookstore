"""Debug with fill() method for login."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def test_with_fill():
    """Try login with fill() method."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        password = "TestPass123!"
        
        # REGISTER with keyboard (since it works)
        print(f"\n📝 Registering: {username}")
        await page.goto(f"{settings.BASE_URL}register", wait_until="networkidle")
        
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
        
        # Gender
        genders = await page.query_selector_all('input[type="radio"]')
        await genders[0].click()  # Click first radio (Male)
        
        #Register button
        register_btns = await page.query_selector_all('button:has-text("Register")')
        await register_btns[-1].click()  # Click last Register btn
        
        await page.wait_for_timeout(3000)
        print(f"✅ Registered. URL: {page.url}")
        
        # LOGIN with fill() method
        print(f"\n🔐 Logging in with fill()...")
        
        # Make sure we're on login page
        if "login" not in page.url.lower():
            print(f"   Not on login page, navigating...")
            await page.goto(f"{settings.BASE_URL}login", wait_until="networkidle")
        
        # Use fill() instead of keyboard
        print(f"   Filling username with fill()...")
        await page.fill('input[formcontrolname="username"]', username)
        
        print(f"   Filling password with fill()...")
        await page.fill('input[formcontrolname="password"]', password)
        
        await page.wait_for_timeout(1000)
        
        # Verify fields
        username_val = await page.input_value('input[formcontrolname="username"]')
        password_val = await page.input_value('input[formcontrolname="password"]')
        print(f"   Username: {username_val}")
        print(f"   Password: {password_val}")
        
        # Try clicking button
        print(f"\n   Clicking Login button...")
        login_btns = await page.query_selector_all('button:has-text("Login")')
        if login_btns:
            await login_btns[-1].click()  # Try last button
            await page.wait_for_timeout(2000)
            print(f"   URL after click: {page.url}")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_with_fill())
