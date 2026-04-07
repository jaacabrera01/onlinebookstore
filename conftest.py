import pytest
import asyncio
from pathlib import Path
from typing import Generator, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from config import get_settings


settings = get_settings()


@pytest.fixture(params=settings.BROWSERS)
async def browser(request) -> Generator[Browser, None, None]:
    """Create a browser instance."""
    browser_type = request.param
    async with async_playwright() as p:
        browser = await p.__getattribute__(browser_type).launch(
            headless=settings.HEADLESS,
            slow_mo=settings.SLOW_MO,
        )
        yield browser
        await browser.close()


@pytest.fixture
async def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """Create a browser context with tracing enabled."""
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True,
    )
    
    # Record trace for debugging
    await context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True
    )
    
    yield context
    
    # Stop tracing and save
    trace_path = Path(settings.SCREENSHOT_DIR) / f"trace-{asyncio.current_task().get_name() if asyncio.current_task() else 'default'}.zip"
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    
    await context.close()


@pytest.fixture
async def page(context: BrowserContext) -> Generator[Page, None, None]:
    """Create a page instance with auto-waiting enabled."""
    page = await context.new_page()
    page.set_default_timeout(settings.TIMEOUT)
    page.set_default_navigation_timeout(settings.NAVIGATION_TIMEOUT)
    
    yield page
    
    # Take screenshot on failure
    if settings.SCREENSHOT_ON_FAILURE:
        screenshot_dir = Path(settings.SCREENSHOT_DIR)
        screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    await page.close()


@pytest.fixture
async def authenticated_page(page: Page) -> Generator[Page, None, None]:
    """Create an authenticated page (must be configured with valid credentials)."""
    # Navigate to login
    await page.goto(f"{settings.BASE_URL}login")
    
    # Fill login form - using data-test-id when available, otherwise user-facing attributes
    await page.fill('input[type="email"]', settings.TEST_USERNAME)
    await page.fill('input[type="password"]', settings.TEST_PASSWORD)
    
    # Click login button
    await page.click('button[type="submit"]')
    
    # Wait for navigation
    await page.wait_for_url(f"{settings.BASE_URL}*")
    
    yield page


@pytest.fixture(autouse=True)
def reset_test_data():
    """Reset test data between tests if needed."""
    # This fixture can be used to cleanup test data after each test
    yield


@pytest.fixture
def base_url() -> str:
    """Provide base URL."""
    return settings.BASE_URL


@pytest.fixture
def settings_fixture():
    """Provide settings."""
    return settings
