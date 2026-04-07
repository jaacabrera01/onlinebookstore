"""Debug script to test full flow in single browser instance."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def test_full_flow():
    """Test registration then login in same browser."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        password = "TestPass123!"
        
        # REGISTER
        print(f"\n📝 Step 1: Register user")
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
        await page.wait_for_timeout(2000)
        
        print(f"✅ Registration complete. URL: {page.url}")
        
        # LOGIN
        print(f"\n🔐 Step 2: Login user")
        await page.wait_for_selector('input[formcontrolname="username"]', timeout=5000)
        
        # Clear fields first
        await page.fill('input[formcontrolname="username"]', "")
        await page.fill('input[formcontrolname="password"]', "")
        
        await page.click('input[formcontrolname="username"]')
        await page.keyboard.type(username)
        
        # Check value  
        username_value = await page.input_value('input[formcontrolname="username"]')
        print(f"   Username field value: {username_value}")
        
        await page.click('input[formcontrolname="password"]')
        await page.keyboard.type(password)
        
        # Check value
        password_value = await page.input_value('input[formcontrolname="password"]')
        print(f"   Password field value: {password_value}")
        
        # Wait and check form classes
        await page.wait_for_timeout(1000)
        username_input = await page.query_selector('input[formcontrolname="username"]')
        username_class = await username_input.get_attribute("class")
        print(f"   Username class: {username_class}")
        
        print(f"\n🔘 Step 3: Submit login")
        print(f"   Trying different submission methods...")
        
        # Method 1: Try clicking the Login button
        print(f"   Method 1: Click Login button...")
        login_buttons = await page.query_selector_all('button:has-text("Login")')
        print(f"      Found {len(login_buttons)} Login buttons")
        
        for i, btn in enumerate(login_buttons):
            print(f"      Clicking button {i+1}...")
            await btn.click(force=True)
            await page.wait_for_timeout(1500)
            print(f"      URL: {page.url}")
            
            if "login" not in page.url.lower():
                print(f"      ✅ Login successful!")
                break
        
        if "login" in page.url.lower():
            print(f"\n   Method 2: Press Enter...")
            await page.press('input[formcontrolname="password"]', "Enter")
            await page.wait_for_timeout(2000)
            print(f"      URL: {page.url}")
        
        print(f"\n✅ Final URL: {page.url}")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_full_flow())
