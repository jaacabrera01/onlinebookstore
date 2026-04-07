# BookCart Automation Testing Framework - Complete Setup

## 🎉 Project Successfully Created!

Your comprehensive test automation framework for BookCart is ready. This document provides step-by-step instructions to get started.

## 📦 What You Have

A production-ready test automation framework with:

- **51+ automated tests** covering all critical paths
- **6 test suites** organized by feature
- **6 page objects** for clean test code
- **2 workflow files** for GitHub Actions CI/CD
- **Complete documentation** and guides
- **Docker support** for containerized testing
- **Makefile** with common commands

## 🚀 Getting Started (5 Minutes)

### Step 1: Install Dependencies

**Option A: Automatic Setup (Recommended)**

**macOS/Linux:**
```bash
cd "/Users/jaacabrera/Documents/Python Scripts/Online Bookstore"
bash setup.sh
```

**Windows:**
```bash
cd "C:\Users\...\Documents\Python Scripts\Online Bookstore"
setup.bat
```

**Option B: Manual Setup**

```bash
# Navigate to project
cd "/Users/jaacabrera/Documents/Python Scripts/Online Bookstore"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install
python -m playwright install-deps
```

### Step 2: Run Your First Tests

```bash
# Run smoke tests (critical path - 3 minutes)
pytest -m smoke -v

# OR run all tests
pytest tests/ -v

# OR use Makefile
make smoke
```

### Step 3: View Test Report

```bash
# Generate Allure report
pytest tests/ --alluredir=allure-results
allure serve allure-results

# OR use Makefile
make report
```

## 📋 Project Structure

```
Online Bookstore/                    Root directory
├── README.md                        Main documentation
├── GETTING_STARTED.md               This file
├── QUICKSTART.md                    Quick reference
├── TESTING_GUIDE.md                 Best practices
├── requirements.txt                 Python dependencies
├── pytest.ini                       Pytest configuration
├── pyproject.toml                   Project metadata
├── config.py                        Settings & configuration
├── conftest.py                      Pytest fixtures
│
├── pages/                           Page Object Models
│   ├── __init__.py                 Base page class
│   ├── home_page.py                Homepage
│   ├── login_page.py               Login page
│   ├── register_page.py            Registration
│   ├── product_detail_page.py      Product page
│   ├── cart_page.py                Shopping cart
│   ├── checkout_page.py            Checkout
│   └── README.md                   Page object docs
│
├── tests/                           Test suites (51+ tests)
│   ├── test_authentication.py      Login tests (13)
│   ├── test_product_search.py      Search tests (7)
│   ├── test_shopping_cart.py       Cart tests (6)
│   ├── test_checkout.py            Checkout tests (8)
│   ├── test_api.py                 API tests (9)
│   └── test_visual_regression.py   Visual tests (8)
│
├── utils/                           Utilities
│   ├── __init__.py                 Logging utilities
│   ├── api_client.py               API testing client
│   └── visual_regression.py        Visual testing tools
│
├── .github/workflows/              GitHub Actions
│   ├── tests.yml                   Main test workflow
│   └── regression-tests.yml        Scheduled regression
│
├── setup.sh                         macOS/Linux setup
├── setup.bat                        Windows setup
├── Makefile                         Common commands
├── Dockerfile                       Docker image
├── docker-compose.yml               Docker compose
├── .env.example                     Environment template
├── .gitignore                       Git ignore rules
└── .dockerignore                    Docker ignore rules
```

## 📚 Documentation Overview

| Document | Purpose | Read Time |
|----------|---------|-----------|
| **README.md** | Complete guide with all details | 15 min |
| **QUICKSTART.md** | Fast reference guide | 5 min |
| **GETTING_STARTED.md** | This setup guide | 10 min |
| **TESTING_GUIDE.md** | Best practices & patterns | 15 min |
| **pages/README.md** | Page object documentation | 10 min |

**Start here:** QUICKSTART.md (5 minutes)

## 🎯 Common Tasks

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific category
pytest -m smoke -v          # Smoke tests (3 min)
pytest -m critical -v       # Critical path (5-10 min)
pytest -m regression -v     # Full regression (30+ min)

# Run specific file
pytest tests/test_authentication.py -v

# Run in parallel (faster)
pytest tests/ -n auto

# Run with detailed output
pytest tests/ -v -s

# Run in headed mode (see browser)
HEADED=true pytest tests/ -v
```

### Generate Reports

```bash
# Generate Allure report
pytest tests/ --alluredir=allure-results
allure serve allure-results

# Generate coverage report
pytest tests/ --cov=pages --cov=utils --cov-report=html
open htmlcov/index.html
```

### Use Makefile

```bash
make help           # Show all commands
make install        # Install dependencies
make test           # Run all tests
make smoke          # Run smoke tests
make critical       # Run critical tests
make report         # Generate Allure report
make clean          # Clean artifacts
make docker-test    # Run in Docker
```

## 🔍 What Tests Are Included

### Authentication (13 tests)
- ✅ Valid login
- ✅ Invalid credentials
- ✅ User registration
- ✅ Email validation
- ✅ Password matching
- And more...

### Product Search (7 tests)
- ✅ Search by title
- ✅ Category filtering
- ✅ No results handling
- ✅ Product navigation
- And more...

### Shopping Cart (6 tests)
- ✅ Add to cart
- ✅ Remove items
- ✅ Update quantities
- ✅ Cart calculations
- And more...

### Checkout (8 tests)
- ✅ Address entry
- ✅ Payment forms
- ✅ Order confirmation
- And more...

### API Testing (9 tests)
- ✅ Product endpoints
- ✅ Cart operations
- ✅ User endpoints
- ✅ Response validation
- And more...

### Visual Regression (8 tests)
- ✅ Layout consistency
- ✅ Cross-browser testing
- ✅ Responsive design
- And more...

## ⚙️ Configuration

### Create .env file

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Application
BASE_URL=https://bookcart.azurewebsites.net/
HEADLESS=true

# Browsers to test (comma-separated)
BROWSERS=chromium,firefox,webkit

# Timeouts (milliseconds)
TIMEOUT=30000
NAVIGATION_TIMEOUT=30000
WAIT_TIMEOUT=10000

# Test credentials (update with real test account)
TEST_USERNAME=testuser@example.com
TEST_PASSWORD=TestPassword123!
```

## 🐳 Docker Usage

### Using Docker Compose (Includes Allure Report)

```bash
# Build and run tests with Allure report
docker-compose up

# Access Allure at http://localhost:4040
```

### Using Docker Manually

```bash
# Build image
docker build -t bookcart-tests .

# Run tests
docker run --rm bookcart-tests

# Run specific tests
docker run --rm bookcart-tests pytest tests/test_authentication.py -v

# Mount local results
docker run --rm \
  -v $(pwd)/allure-results:/app/allure-results \
  bookcart-tests
```

## 🔧 Troubleshooting

### Issue: Python not found

**Solution:**
```bash
# Ensure Python 3.10+ is installed
python --version  # Should be 3.10 or higher
```

### Issue: Playwright browsers not installed

**Solution:**
```bash
playwright install --with-deps
```

### Issue: Tests timeout

**Solution:**
Update timeout in `.env`:
```env
TIMEOUT=60000
NAVIGATION_TIMEOUT=60000
WAIT_TIMEOUT=15000
```

### Issue: Cannot find .env file

**Solution:**
```bash
cp .env.example .env
# Edit .env with your settings
```

### Issue: Tests fail but work locally

Check:
1. Environment variables match
2. BASE_URL is correct
3. Test credentials are valid
4. Browser cache is cleared

## 📖 Next Steps

### Level 1: Run Existing Tests
1. Run smoke tests: `pytest -m smoke -v`
2. Run all tests: `pytest tests/ -v`
3. Generate report: `allure serve allure-results`

### Level 2: Understand Tests
1. Read [QUICKSTART.md](QUICKSTART.md) (5 min)
2. Read [TESTING_GUIDE.md](TESTING_GUIDE.md) (15 min)
3. Review tests in `tests/` directory
4. Review page objects in `pages/` directory

### Level 3: Write Tests
1. Create new test file in `tests/`
2. Use existing page objects
3. Follow AAA pattern (Arrange-Act-Assert)
4. Add meaningful assertions

### Level 4: CI/CD Setup
1. Push to GitHub
2. GitHub Actions automatically runs tests
3. Allure reports generated and published
4. View on GitHub Pages

## 🎓 Example Test

Create `tests/test_example.py`:

```python
import pytest
from pages.home_page import HomePage
from playwright.async_api import Page

class TestExample:
    @pytest.mark.smoke
    async def test_search_functionality(self, page: Page):
        """Test that users can search for books."""
        home_page = HomePage(page)
        
        # Go to home page
        await home_page.goto_home()
        
        # Search for a book
        await home_page.search_for_book("Python")
        
        # Verify results
        books = await home_page.get_featured_books_count()
        assert books > 0, "No search results displayed"
```

Run it:
```bash
pytest tests/test_example.py -v
```

## ✨ Key Features

### Smart Test Design
- ✅ Page Object Model pattern
- ✅ No hardcoded waits
- ✅ Dynamic element waiting
- ✅ Test isolation and cleanup

### Comprehensive Assertions
- ✅ URL verification
- ✅ Element visibility
- ✅ Text content checking
- ✅ API response validation

### Multiple Test Categories
- ✅ Smoke tests (3 min)
- ✅ Critical tests (5-10 min)
- ✅ Regression tests (30+ min)
- ✅ API tests
- ✅ Visual tests

### Advanced Features
- ✅ Cross-browser testing
- ✅ CI/CD integration
- ✅ Visual regression
- ✅ Allure reporting
- ✅ Docker support

## 📊 Test Statistics

| Metric | Value |
|--------|-------|
| **Total Tests** | 51+ |
| **Page Objects** | 6 |
| **Test Suites** | 6 |
| **Lines of Test Code** | 1000+ |
| **Coverage** | All critical paths |
| **Documentation** | 5 guides |

## 🎯 Success Checklist

After setup, verify:

- [ ] Python 3.10+ installed
- [ ] Dependencies installed
- [ ] Playwright installed
- [ ] `.env` file created
- [ ] Smoke tests pass
- [ ] Allure report generated
- [ ] No import errors
- [ ] Can create new test file

## 🆘 Need Help?

1. **Quick Start:** See [QUICKSTART.md](QUICKSTART.md)
2. **Run Tests:** `pytest -m smoke -v`
3. **Common Issues:** See [README.md](README.md#troubleshooting)
4. **Test Writing:** See [TESTING_GUIDE.md](TESTING_GUIDE.md)
5. **Page Objects:** See [pages/README.md](pages/README.md)

## 📞 Support Resources

- Playwright Docs: https://playwright.dev/python/
- Pytest Docs: https://docs.pytest.org/
- Allure Docs: https://docs.qameta.io/allure/
- BookCart App: https://bookcart.azurewebsites.net/

## 🎉 You're All Set!

The framework is complete and ready to use. Start with:

```bash
pytest -m smoke -v
```

Then read the guides and begin writing your own tests!

---

**Happy Testing!** 🚀

For detailed information, see [README.md](README.md).
