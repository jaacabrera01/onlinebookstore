"""Debug selectors on home and register pages."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def debug_selectors():
    """Check what selectors actually exist on the pages."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Check home page
        print("\n📄 HOME PAGE SELECTORS")
        print("=" * 50)
        await page.goto(f"{settings.BASE_URL}", wait_until="domcontentloaded")
        
        # Look for search input
        search_inputs = await page.query_selector_all("input")
        for i, inp in enumerate(search_inputs[:3]):
            placeholder = await inp.get_attribute("placeholder")
            formcontrol = await inp.get_attribute("formcontrolname")
            type_attr = await inp.get_attribute("type")
            print(f"Input {i}: type={type_attr}, placeholder={placeholder}, formcontrol={formcontrol}")
        
        # Look for books
        books = await page.query_selector_all(".book-item, [class*='book'], [class*='product']")
        print(f"Books found with .book-item: {len(books)}")
        
        # Register page
        print("\n📄 REGISTER PAGE SELECTORS")
        print("=" * 50)
        await page.goto(f"{settings.BASE_URL}register", wait_until="domcontentloaded")
        
        # Look for form inputs
        inputs = await page.query_selector_all("input")
        print(f"Total inputs found: {len(inputs)}")
        for i, inp in enumerate(inputs[:10]):
            placeholder = await inp.get_attribute("placeholder")
            formcontrol = await inp.get_attribute("formcontrolname")
            type_attr = await inp.get_attribute("type")
            name = await inp.get_attribute("name")
            print(f"Input {i}: type={type_attr}, placeholder={placeholder}, formcontrol={formcontrol}, name={name}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_selectors())
