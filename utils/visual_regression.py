"""Visual regression testing utilities."""
from pathlib import Path
from playwright.async_api import Page
from config import get_settings


settings = get_settings()


class VisualRegression:
    """Handle visual regression testing."""
    
    def __init__(self):
        self.baseline_dir = Path("tests/visual/baselines")
        self.actual_dir = Path("tests/visual/actuals")
        self.diff_dir = Path("tests/visual/diffs")
        
        # Create directories
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        self.actual_dir.mkdir(parents=True, exist_ok=True)
        self.diff_dir.mkdir(parents=True, exist_ok=True)
    
    async def take_screenshot(
        self,
        page: Page,
        name: str,
        full_page: bool = False
    ) -> str:
        """Take a screenshot."""
        screenshot_path = self.actual_dir / f"{name}.png"
        await page.screenshot(
            path=screenshot_path,
            full_page=full_page,
            mask_color="#ddd"  # Mask dynamic content
        )
        return str(screenshot_path)
    
    async def compare_screenshot(
        self,
        page: Page,
        name: str,
        full_page: bool = False,
        max_diff_pixels: int = 100,
        threshold: float = 0.1
    ) -> bool:
        """
        Compare current screenshot with baseline.
        
        Args:
            page: Playwright page
            name: Screenshot name
            full_page: Capture full page
            max_diff_pixels: Max pixels allowed to differ
            threshold: Threshold for pixel difference (0.0-1.0)
        
        Returns:
            True if screenshots match, False otherwise
        """
        actual_path = self.actual_dir / f"{name}.png"
        baseline_path = self.baseline_dir / f"{name}.png"
        
        # Take actual screenshot
        await page.screenshot(
            path=actual_path,
            full_page=full_page,
            mask_color="#ddd"
        )
        
        # If baseline doesn't exist, create it
        if not baseline_path.exists():
            actual_path.rename(baseline_path)
            return True
        
        # Compare using Playwright's built-in comparison
        try:
            await page.expect_screenshot(
                name=f"{name}.png",
                path=baseline_path,
                full_page=full_page,
                max_diff_pixels=max_diff_pixels,
                threshold=threshold
            )
            return True
        except AssertionError:
            return False
    
    def get_baseline_path(self, name: str) -> Path:
        """Get baseline screenshot path."""
        return self.baseline_dir / f"{name}.png"
    
    def get_actual_path(self, name: str) -> Path:
        """Get actual screenshot path."""
        return self.actual_dir / f"{name}.png"
