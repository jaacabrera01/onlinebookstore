import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)
    
    # Application
    BASE_URL: str = "https://bookcart.azurewebsites.net/"
    HEADLESS: bool = True
    SLOW_MO: int = 500
    
    # Chrome 
    BROWSERS: list = ["chromium"]  # Options: chromium, firefox, webkit
    
    def __init__(self, **data):
        """Override to ensure BROWSERS is always chromium-only."""
        super().__init__(**data)
        # Force chromium only, ignore environment variables
        self.BROWSERS = ["chromium"]
    
    # Timeouts
    TIMEOUT: int = 30000  # milliseconds
    NAVIGATION_TIMEOUT: int = 30000
    WAIT_TIMEOUT: int = 10000
    
    # Screenshots
    SCREENSHOT_ON_FAILURE: bool = True
    SCREENSHOT_DIR: str = "test-results/screenshots"
    
    # Allure
    ALLURE_RESULTS_DIR: str = "allure-results"
    
    # Test data (loaded from environment variables)
    TEST_USERNAME: str = "jaacabrera"
    TEST_PASSWORD: str = ""  # Set via environment variable
    
    # API Configuration
    API_BASE_URL: str = "https://bookcart.azurewebsites.net/api"
    API_ADMIN_USERNAME: str = "admin"
    API_ADMIN_PASSWORD: str = ""  # Set via environment variable
    API_TIMEOUT: int = 30
    
    # Selectors strategy
    WAIT_FOR_ELEMENT_TIMEOUT: int = 10000


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


# Create directories if they don't exist
def ensure_directories():
    """Ensure required directories exist."""
    screenshot_dir = Path(get_settings().SCREENSHOT_DIR)
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    
    allure_dir = Path(get_settings().ALLURE_RESULTS_DIR)
    allure_dir.mkdir(parents=True, exist_ok=True)


ensure_directories()
