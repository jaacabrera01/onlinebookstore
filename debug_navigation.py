"""Debug script to test navigation URLs."""
import asyncio
from playwright.async_api import async_playwright
from config import get_settings

settings = get_settings()


async def test_navigation():
    """Test navigation to different pages."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page()
        
        # Test 1: Navigate to login
        print(f"\n🔗 Test 1: Navigating to login")
        print(f"   BASE_URL: {settings.BASE_URL}")
        print(f"   Endpoint: login")
        url = f"{settings.BASE_URL.rstrip('/')}/login"
        print(f"   Full URL: {url}")
        await page.goto(url)
        await page.wait_for_load_state("domcontentloaded")
        current = page.url
        print(f"   Current URL: {current}")
        
        # Test 2: Navigate to register  
        print(f"\n🔗 Test 2: Navigating to register")
        url = f"{settings.BASE_URL.rstrip('/')}/register"
        print(f"   Full URL: {url}")
        await page.goto(url)
        await page.wait_for_load_state("domcontentloaded")
        current = page.url
        print(f"   Current URL: {current}")
        
        await page.wait_for_timeout(3000)
        await browser.close()


if __name__ == "__main__":
    asyncio.run(test_navigation())
