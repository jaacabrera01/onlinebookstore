"""Debug page loading and selectors."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def check_pages():
    """Check if pages load correctly."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Check home page
        print("\n📄 HOME PAGE")
        await page.goto(f"{settings.BASE_URL}", wait_until="load")
        await page.wait_for_timeout(2000)
        print(f"URL: {page.url}")
        
        # Count inputs
        inputs = await page.query_selector_all("input")
        print(f"Inputs on page: {len(inputs)}")
        for i, inp in enumerate(inputs):
            t = await inp.get_attribute("type")
            p_val = await inp.get_attribute("placeholder")
            print(f"  {i}: type={t}, placeholder={p_val}")
        
        # Count items that might be books
        items = await page.query_selector_all('[class*="item"], [class*="book"], [class*="product"]')
        print(f"Item-like elements: {len(items)}")
        
        # Check register page
        print("\n📄 REGISTER PAGE")
        await page.goto(f"{settings.BASE_URL}register", wait_until="load")
        await page.wait_for_timeout(2000)
        print(f"URL: {page.url}")
        
        # Check for formcontrolname
        form_inputs = await page.query_selector_all("[formcontrolname]")
        print(f"Inputs with formcontrolname: {len(form_inputs)}")
        for inp in form_inputs:
            fcn = await inp.get_attribute("formcontrolname")
            print(f"  - formcontrolname={fcn}")
        
        await browser.close()


if __name__ == "__main__":
    asyncio.run(check_pages())
