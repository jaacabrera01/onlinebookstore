.PHONY: help install test smoke critical regression api visual clean report

help:
	@echo "BookCart Test Automation - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install              Install dependencies"
	@echo "  make install-browsers     Install Playwright browsers"
	@echo ""
	@echo "Testing:"
	@echo "  make test                 Run all tests"
	@echo "  make smoke                Run smoke tests (critical path)"
	@echo "  make critical             Run critical tests"
	@echo "  make regression           Run full regression suite"
	@echo "  make api                  Run API tests only"
	@echo "  make visual               Run visual regression tests"
	@echo ""
	@echo "Reporting:"
	@echo "  make report               Generate and serve Allure report"
	@echo "  make coverage             Generate coverage report"
	@echo ""
	@echo "Quality:"
	@echo "  make lint                 Run linting (flake8)"
	@echo "  make format               Format code with Black"
	@echo "  make format-check         Check formatting with Black"
	@echo "  make type-check           Run type checking (mypy)"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean                Remove test artifacts"
	@echo "  make clean-all            Remove all generated files"

# Installation
install:
	pip install -r requirements.txt

install-browsers:
	playwright install
	playwright install-deps

# Testing
test:
	pytest tests/ -v

smoke:
	pytest -m smoke -v

critical:
	pytest -m critical -v

regression:
	pytest -m regression -v

api:
	pytest tests/test_api.py -v

visual:
	pytest tests/test_visual_regression.py -v

test-parallel:
	pytest tests/ -v -n auto

test-headed:
	HEADLESS=false pytest tests/ -v

# Reporting
report:
	pytest tests/ --alluredir=allure-results
	allure serve allure-results

coverage:
	pytest tests/ --cov=pages --cov=utils --cov-report=html
	@echo "Coverage report generated in htmlcov/"

# Quality
lint:
	flake8 tests/ pages/ utils/ --max-line-length=100

format:
	black tests/ pages/ utils/ config.py conftest.py

format-check:
	black --check tests/ pages/ utils/ config.py conftest.py

type-check:
	mypy tests/ pages/ utils/ --ignore-missing-imports

quality: format lint type-check
	@echo "Quality checks completed"

# Cleanup
clean:
	rm -rf allure-results/ allure-report/ htmlcov/ .coverage
	rm -rf test-results/ logs/
	rm -rf .pytest_cache/ __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

clean-all: clean
	rm -rf .venv/ venv/ *.egg-info/
	rm -rf .pytest_cache/ .mypy_cache/

# Development
dev-setup: install install-browsers
	@echo "Development environment ready"

dev-test: format lint
	pytest tests/ -v --tb=short

# CI/CD
ci-test:
	pytest tests/ --tb=short --alluredir=allure-results -m "smoke or critical"

ci-full:
	pytest tests/ --tb=short --alluredir=allure-results

# Docker (if using Docker)
docker-build:
	docker build -t bookcart-tests .

docker-test:
	docker run --rm bookcart-tests make test

# Utilities
check-browsers:
	@python -c "from playwright.async_api import async_playwright; import asyncio; asyncio.run(_check_browsers())" || true

_check_browsers:
	@python << 'EOF'
import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        print("Installed browsers:")
        for browser_type in ["chromium", "firefox", "webkit"]:
            try:
                browser = await getattr(p, browser_type).launch()
                print(f"✓ {browser_type}")
                await browser.close()
            except Exception as e:
                print(f"✗ {browser_type}: {e}")

asyncio.run(check())
EOF

update-deps:
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

check-env:
	@python << 'EOF'
from config import get_settings
settings = get_settings()
print("Configuration:")
print(f"  Base URL: {settings.BASE_URL}")
print(f"  Headless: {settings.HEADLESS}")
print(f"  Browsers: {settings.BROWSERS}")
print(f"  Timeout: {settings.TIMEOUT}ms")
EOF

# Statistics
stats:
	@echo "Test Statistics:"
	@find tests -name "*.py" -type f | xargs wc -l | tail -1
	@echo ""
	@echo "Test Files:"
	@find tests -name "test_*.py" -type f | wc -l
	@echo ""
	@echo "Page Objects:"
	@find pages -name "*_page.py" -type f | wc -l
