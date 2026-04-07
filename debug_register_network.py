"""Debug script to monitor network during registration."""
import asyncio
import uuid
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def debug_with_network():
    """Debug registration with network monitoring."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        password = "TestPass123!"
        
        # Monitor requests
        responses = []
        def on_response(resp):
            responses.append({
                'url': resp.url,
                'status': resp.status,
                'method': resp.status
            })
            print(f"   📡 Response: {resp.status} {resp.url}")
        
        page.on("response", on_response)
        
        # Navigate
        print(f"\n🔗 Navigating to register page...")
        await page.goto(f"{settings.BASE_URL}register")
        await page.wait_for_load_state("networkidle")
        
        # Fill form
        print(f"\n✍️ Filling form...")
        await page.fill('input[formcontrolname="firstName"]', "Test")
        await page.fill('input[formcontrolname="lastName"]', "User")
        await page.fill('input[formcontrolname="userName"]', username)
        await page.fill('input[formcontrolname="password"]', password)
        await page.fill('input[formcontrolname="confirmPassword"]', password)
        print(f"✅ Form filled")
        
        # Click Register and intercept the request
        print(f"\n🔘 Clicking Register button...")
        
        async def click_and_wait():
            await page.click('button:has-text("Register")')
            try:
                # Wait for any navigation or network activity
                await page.wait_for_load_state("networkidle", timeout=5000)
            except:
                print(f"   (No network activity detected)")
        
        await click_and_wait()
        
        print(f"\n📊 Network activity:")
        if responses:
            for resp in responses[-5:]:  # Last 5 responses
                print(f"   {resp['status']} - {resp['url']}")
        else:
            print(f"   No responses captured")
        
        print(f"\n📍 Final URL: {page.url}")
        
        # Check page state
        print(f"\n🔍 Page state:")
        title = await page.title()
        print(f"   Title: {title}")
        
        # Check if success message appears
        body_text = await page.text_content("body")
        if "successfully" in body_text.lower():
            print(f"   ✅ Success message detected")
        if "error" in body_text.lower():
            print(f"   ❌ Error detected in page")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_with_network())
