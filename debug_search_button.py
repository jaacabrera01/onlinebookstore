"""Check search button."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def check_search_button():
    """Check for search button."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("\n📄 HOME PAGE - LOOKING FOR SEARCH BUTTON")
        await page.goto(f"{settings.BASE_URL}", wait_until="load")
        await page.wait_for_timeout(2000)
        
        # Check all buttons
        buttons = await page.query_selector_all("button")
        print(f"Total buttons on page: {len(buttons)}")
        
        for i, btn in enumerate(buttons):
            text = await btn.text_content()
            aria = await btn.get_attribute("aria-label")
            type_attr = await btn.get_attribute("type")
            classes = await btn.get_attribute("class")
            if text or aria:
                print(f"  Button {i}: text='{text}', aria='{aria}', type='{type_attr}'")
        
        # Try filling search and check buttons again
        print("\n📝 After filling search input:")
        await page.fill('input[placeholder="Search books or authors"]', "Python")
        buttons = await page.query_selector_all("button")
        for i, btn in enumerate(buttons):
            text = await btn.text_content()
            aria = await btn.get_attribute("aria-label")
            if text or aria:
                print(f"  Button {i}: text='{text}', aria='{aria}'")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_search_button())
