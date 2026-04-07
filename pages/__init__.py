"""Base page object for all pages."""
from playwright.async_api import Page
from config import get_settings


settings = get_settings()


class BasePage:
    """Base class for all page objects with common functionality."""
    
    def __init__(self, page: Page):
        self.page = page
        self.base_url = settings.BASE_URL
    
    async def goto(self, endpoint: str = ""):
        """Navigate to page."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        await self.page.goto(url, wait_until="domcontentloaded")
    
    async def is_visible(self, selector: str, timeout: int = settings.WAIT_TIMEOUT) -> bool:
        """Check if element is visible."""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout, state="visible")
            return True
        except Exception:
            return False
    
    async def wait_for_element(self, selector: str, timeout: int = settings.WAIT_TIMEOUT):
        """Wait for element to be visible."""
        await self.page.wait_for_selector(selector, timeout=timeout, state="visible")
    
    async def click(self, selector: str):
        """Click element."""
        await self.page.click(selector)
    
    async def fill(self, selector: str, text: str):
        """Fill input field."""
        await self.page.fill(selector, text)
    
    async def get_text(self, selector: str) -> str:
        """Get element text."""
        return await self.page.text_content(selector) or ""
    
    async def get_attribute(self, selector: str, attribute: str) -> str:
        """Get element attribute."""
        return await self.page.get_attribute(selector, attribute) or ""
    
    async def press_key(self, selector: str, key: str):
        """Press key on element."""
        await self.page.press(selector, key)
    
    async def select_option(self, selector: str, value: str):
        """Select dropdown option."""
        await self.page.select_option(selector, value)
    
    async def get_url(self) -> str:
        """Get current URL."""
        return self.page.url
    
    async def take_screenshot(self, name: str) -> str:
        """Take screenshot."""
        path = f"test-results/screenshots/{name}.png"
        await self.page.screenshot(path=path)
        return path
    
    async def wait_for_navigation(self, callback):
        """Wait for navigation."""
        async with self.page.expect_navigation():
            await callback()
    
    async def wait_for_url_change(self, timeout: int = settings.TIMEOUT):
        """Wait for URL to change."""
        await self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    async def get_page_title(self) -> str:
        """Get page title."""
        return await self.page.title()
    
    async def is_element_enabled(self, selector: str) -> bool:
        """Check if element is enabled."""
        return await self.page.is_enabled(selector)
    
    async def is_element_checked(self, selector: str) -> bool:
        """Check if checkbox is checked."""
        return await self.page.is_checked(selector)
    
    async def check_element(self, selector: str):
        """Check checkbox."""
        await self.page.check(selector)
    
    async def uncheck_element(self, selector: str):
        """Uncheck checkbox."""
        await self.page.uncheck(selector)
    
    async def scroll_to_element(self, selector: str):
        """Scroll to element."""
        await self.page.locator(selector).scroll_into_view_if_needed()
    
    async def wait_for_api_call(self, method: str = "GET", path_pattern: str = ""):
        """Wait for API call and return it."""
        async with self.page.expect_response(
            lambda response: method in response.request.method.upper() and path_pattern in response.url
        ) as response_info:
            await self.page.wait_for_load_state("networkidle")
        return await response_info.value

