"""Debug script to find the gender field."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def find_gender_field():
    """Find the gender field selector."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        # Navigate to register page
        await page.goto(f"{settings.BASE_URL}register")
        await page.wait_for_load_state("networkidle")
        
        print(f"\n🔍 Looking for gender field...")
        
        # Look for select elements
        selects = await page.query_selector_all("select")
        print(f"\n📋 Found {len(selects)} select elements:")
        for i, sel in enumerate(selects):
            name = await sel.get_attribute("name")
            formcontrol = await sel.get_attribute("formcontrolname")
            print(f"   Select {i+1}: name={name}, formcontrolname={formcontrol}")
            
            # Get options
            options = await sel.query_selector_all("option")
            for opt in options[:5]:
                opt_text = await opt.text_content()
                print(f"      - {opt_text.strip()}")
        
        # Look for radio buttons
        radios = await page.query_selector_all('input[type="radio"]')
        print(f"\n📻 Found {len(radios)} radio buttons:")
        for i, radio in enumerate(radios[:5]):
            name = await radio.get_attribute("name")
            formcontrol = await radio.get_attribute("formcontrolname")
            value = await radio.get_attribute("value")
            print(f"   Radio {i+1}: name={name}, formcontrolname={formcontrol}, value={value}")
        
        # Look for mat-select (Angular Material)
        mat_selects = await page.query_selector_all("mat-select, [role='listbox']")
        print(f"\n🎯 Found {len(mat_selects)} mat-select elements:")
        for i, ms in enumerate(mat_selects[:3]):
            formcontrol = await ms.get_attribute("formcontrolname")
            aria_label = await ms.get_attribute("aria-label")
            print(f"   Mat-select {i+1}: formcontrolname={formcontrol}, aria-label={aria_label}")
            
            # Try to get text content
            text = await ms.text_content()
            print(f"      Text: {text.strip()[:50]}")
        
        # Look for any label with "gender"
        labels = await page.query_selector_all("label")
        print(f"\n🏷️ Labels containing 'gender':")
        for label in labels:
            text = await label.text_content()
            if "gender" in text.lower():
                print(f"   Found: {text.strip()}")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(find_gender_field())
