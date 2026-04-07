"""Debug script to find login button selector."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def find_button():
    """Find the login button selector."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # Navigate to login page
        await page.goto(f"{settings.BASE_URL}login")
        await page.wait_for_load_state("domcontentloaded")
        
        # Get all buttons on the form
        buttons = await page.locator("button").all()
        
        print(f"\n✅ Found {len(buttons)} buttons on the page:\n")
        
        for i, button in enumerate(buttons):
            text = await button.text_content()
            html = await button.get_attribute("outerHTML")
            print(f"Button {i + 1}:")
            print(f"  Text: {text.strip() if text else 'No text'}")
            print(f"  HTML: {html[:150]}...")
            print()
        
        # Keep browser open for 10 seconds
        await page.wait_for_timeout(10000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(find_button())
