"""Allure reporting configuration."""
import pytest
from datetime import datetime
from pathlib import Path


def pytest_configure(config):
    """Configure pytest and allure settings."""
    _ = config  # Unused but required for hook
    
    # Create allure results directory
    allure_results_dir = Path("allure-results")
    allure_results_dir.mkdir(exist_ok=True)
    
    # Create environment properties file for Allure
    env_file = allure_results_dir / "environment.properties"
    with open(env_file, "w") as f:
        f.write(f"Test.Execution.Date={datetime.now().isoformat()}\n")
        f.write(f"Executor=GitHub Actions\n")
        f.write(f"BaseURL=https://bookcart.azurewebsites.net/\n")
        f.write(f"Browser=Chromium, Firefox, WebKit\n")
        f.write(f"Python.Version=3.10+\n")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Add test results to allure report."""
    outcome = yield
    
    if outcome.excinfo is not None and call.when == "call":
        # Test failed
        pass
