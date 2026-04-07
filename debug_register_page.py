"""Debug script to inspect the register page."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def inspect_register_page():
    """Inspect the register page structure."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        # Navigate to register page
        print(f"\n🔗 Navigating to: {settings.BASE_URL}register")
        await page.goto(f"{settings.BASE_URL}register")
        await page.wait_for_load_state("networkidle")
        
        current_url = page.url
        print(f"✅ Actual URL: {current_url}")
        
        # Check for form fields
        print("\n🔍 Checking for form fields:")
        fields = [
            'input[formcontrolname="firstName"]',
            'input[formcontrolname="lastName"]',
            'input[formcontrolname="username"]',
            'input[formcontrolname="email"]',
            'input[formcontrolname="password"]',
            'input[formcontrolname="confirmPassword"]',
        ]
        
        for field in fields:
            try:
                await page.wait_for_selector(field, timeout=2000)
                print(f"   ✅ Found: {field}")
            except:
                print(f"   ❌ NOT found: {field}")
        
        # Get page title
        title = await page.title()
        print(f"\n📄 Page title: {title}")
        
        # Get all inputs on page
        inputs = await page.query_selector_all("input")
        print(f"\n📝 Total inputs on page: {len(inputs)}")
        
        if inputs:
            for i, inp in enumerate(inputs[:5]):
                input_type = await inp.get_attribute("type")
                name = await inp.get_attribute("name")
                placeholder = await inp.get_attribute("placeholder")
                formcontrol = await inp.get_attribute("formcontrolname")
                print(f"   Input {i+1}: type={input_type}, name={name}, placeholder={placeholder}, formcontrolname={formcontrol}")
        
        # Check for buttons
        buttons = await page.query_selector_all("button")
        print(f"\n🔘 Total buttons on page: {len(buttons)}")
        
        if buttons:
            for i, btn in enumerate(buttons[:5]):
                text = await btn.text_content()
                print(f"   Button {i+1}: {text}")
        
        await page.wait_for_timeout(5000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(inspect_register_page())
