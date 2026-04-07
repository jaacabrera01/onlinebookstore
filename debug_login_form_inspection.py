"""Debug script to find all login form elements."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def inspect_login_form():
    """Inspect all elements on the login form."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        # Navigate to login page
        await page.goto(f"{settings.BASE_URL}login")
        await page.wait_for_load_state("networkidle")
        
        print(f"\n🔍 Inspecting login form...")
        
        # Find all form elements
        print(f"\n📝 All inputs:")
        inputs = await page.query_selector_all("input")
        for i, inp in enumerate(inputs):
            inp_type = await inp.get_attribute("type")
            name = await inp.get_attribute("name")
            formcontrol = await inp.get_attribute("formcontrolname")
            placeholder = await inp.get_attribute("placeholder")
            required = await inp.get_attribute("required")
            print(f"   {i+1}. type={inp_type}, formcontrol={formcontrol}, name={name}, placeholder={placeholder}, required={required}")
        
        # Find all buttons
        print(f"\n🔘 All buttons:")
        buttons = await page.query_selector_all("button")
        for i, btn in enumerate(buttons):
            text = await btn.text_content()
            btn_type = await btn.get_attribute("type")
            aria_label = await btn.get_attribute("aria-label")
            print(f"   {i+1}. type={btn_type}, text='{text.strip()}', aria-label={aria_label}")
        
        # Check for form itself
        print(f"\n📋 Forms:")
        forms = await page.query_selector_all("form")
        print(f"   Found {len(forms)} form(s)")
        for i, form in enumerate(forms):
            form_name = await form.get_attribute("name")
            form_id = await form.get_attribute("id")
            print(f"   Form {i+1}: id={form_id}, name={form_name}")
        
        # Check login button more carefully
        print(f"\n🔍 Login button details:")
        login_btn = await page.query_selector('button:has-text("Login")')
        if login_btn:
            btn_class = await login_btn.get_attribute("class")
            btn_disabled = await login_btn.is_disabled()
            btn_type = await login_btn.get_attribute("type")
            print(f"   Type: {btn_type}")
            print(f"   Disabled: {btn_disabled}")
            print(f"   Class: {btn_class}")
            
            # Try to get onClick attribute
            on_click = await login_btn.get_attribute("onclick")
            print(f"   onClick: {on_click}")
        
        # Check for any required fields or validators
        print(f"\n🔐 Check for form control status:")
        username_input = await page.query_selector('input[formcontrolname="username"]')
        password_input = await page.query_selector('input[formcontrolname="password"]')
        
        if username_input:
            classes = await username_input.get_attribute("class")
            print(f"   Username input class: {classes}")
        
        if password_input:
            classes = await password_input.get_attribute("class")
            print(f"   Password input class: {classes}")
        
        await page.wait_for_timeout(2000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(inspect_login_form())
