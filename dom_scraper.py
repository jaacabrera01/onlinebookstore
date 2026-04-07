"""DOM scraper to inspect website structure and find correct selectors."""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from config import get_settings


settings = get_settings()


async def scrape_dom():
    """Scrape DOM from various pages to analyze structure."""
    output_dir = Path("dom_snapshots")
    output_dir.mkdir(exist_ok=True)
    
    pages_to_scrape = {
        "home": "",
        "login": "login",
        "register": "register",
        "products": "products",
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for page_name, endpoint in pages_to_scrape.items():
            try:
                url = f"{settings.BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
                print(f"📄 Scraping {page_name} from {url}")
                
                await page.goto(url, wait_until="domcontentloaded")
                
                # Get full HTML
                html = await page.content()
                
                # Save raw HTML
                html_path = output_dir / f"{page_name}_page.html"
                with open(html_path, "w") as f:
                    f.write(html)
                print(f"   ✅ Saved: {html_path}")
                
                # Extract specific elements for analysis
                inputs = await page.evaluate("""
                    () => {
                        const inputs = Array.from(document.querySelectorAll('input, button, select, textarea, [role="button"]'));
                        return inputs.map(el => ({
                            tag: el.tagName,
                            type: el.type || '',
                            id: el.id || '',
                            name: el.name || '',
                            class: el.className || '',
                            placeholder: el.placeholder || '',
                            'data-testid': el.getAttribute('data-testid') || '',
                            text: el.textContent?.trim().substring(0, 50) || '',
                            xpath: getXPath(el)
                        }));
                        
                        function getXPath(element) {
                            if (element.id !== '')
                                return "//*[@id='" + element.id + "']";
                            if (element === document.body)
                                return element.tagName.toLowerCase();
                            
                            var ix = 0;
                            var siblings = element.parentNode.childNodes;
                            for (var i = 0; i < siblings.length; i++) {
                                var sibling = siblings[i];
                                if (sibling === element)
                                    return getXPath(element.parentNode) + "/" + element.tagName.toLowerCase() + "[" + (ix + 1) + "]";
                                if (sibling.nodeType === 1 && sibling.tagName.toLowerCase() === element.tagName.toLowerCase())
                                    ix++;
                            }
                        }
                    }
                """)
                
                # Save element analysis
                analysis_path = output_dir / f"{page_name}_elements.json"
                with open(analysis_path, "w") as f:
                    json.dump(inputs, f, indent=2)
                print(f"   ✅ Elements saved: {analysis_path}")
                
            except Exception as e:
                print(f"   ❌ Error scraping {page_name}: {e}")
        
        await browser.close()
    
    print("\n✅ DOM scraping completed!")
    print(f"📁 Snapshots saved in: {output_dir.absolute()}")
    print("\nReview the HTML files and element analysis to identify correct selectors.")


if __name__ == "__main__":
    asyncio.run(scrape_dom())
