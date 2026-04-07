"""Debug with JavaScript form submission."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def test_with_javascript():
    """Try submitting form via JavaScript."""
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
        
        await page.wait_for_timeout(3000)
        print(f"✅ Registered. URL: {page.url}")
        
        # LOGIN
        print(f"\n🔐 Logging in...")
        
        await page.click('input[formcontrolname="username"]')
        await page.keyboard.type(username)
        await page.click('input[formcontrolname="password"]')
        await page.keyboard.type(password)
        
        await page.wait_for_timeout(1000)
        
        # Try JavaScript form submission
        print(f"   Method 1: Direct form.submit()...")
        forms = await page.query_selector_all("form")
        print(f"   Found {len(forms)} forms")
        
        for i, form in enumerate(forms):
            # Check if form has login inputs
            inputs = await form.query_selector_all("input[formcontrolname]")
            if len(inputs) >= 2:
                print(f"   Form {i} has {len(inputs)} form inputs - submitting...")
                try:
                    await page.evaluate("(f) => f.submit()", form)
                    await page.wait_for_timeout(2000)
                    print(f"   URL: {page.url}")
                    break
                except Exception as e:
                    print(f"   Error: {e}")
        
        if "login" in page.url.lower():
            # Try Method 2: Trigger ng-submit manually
            print(f"\n   Method 2: Trigger ng-submit handler...")
            await page.evaluate("""
                () => {
                    // Try to find and trigger the submit button's click event
                    const loginBtns = document.querySelectorAll('button');
                    for (let btn of loginBtns) {
                        if (btn.textContent.includes('Login')) {
                            console.log('Triggering click on:', btn.textContent);
                            btn.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
                            break;
                        }
                    }
                }
            """)
            await page.wait_for_timeout(2000)
            print(f"   URL: {page.url}")
        
        if "login" in page.url.lower():
            # Method 3: Try finding submit button by type
            print(f"\n   Method 3: Look for submit button...")
            submit_btns = await page.query_selector_all('button[type="submit"]')
            print(f"   Found {len(submit_btns)} submit buttons")
            
            for btn in submit_btns:
                text = await btn.text_content()
                print(f"   Submit button: {text.strip()}")
                await btn.click()
                await page.wait_for_timeout(2000)
                print(f"   URL: {page.url}")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_with_javascript())
