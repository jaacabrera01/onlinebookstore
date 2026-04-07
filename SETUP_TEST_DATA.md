# BookCart Test Data Setup Guide

## Current Status

✅ **Working:**
- Authentication tests (Login/Register) - **6/6 passing**
- Search functionality
- Visual regression tests
- API infrastructure

❌ **Blocked (No Test Data):**
- Shopping cart tests
- Checkout tests
- Featured books tests

⚠️ **API Issues:**
- Books endpoint returns 500 error
- Needs investigation or database reset

## Problem

The BookCart database currently has **no books**, which is why shopping cart and product tests are failing.

## Solutions

### Option 1: Manual UI Entry (Easiest)
1. Open https://bookcart.azurewebsites.net/
2. Look for an Add Book / Admin panel
3. Add 3-5 books manually
4. Run tests - they will now pass

### Option 2: Database Reset/Seed
If there's a database administration tool:
1. Reset the database
2. Run any seed scripts provided
3. Verify books appear in API: `GET https://bookcart.azurewebsites.net/api/Book`

### Option 3: API Direct Population (Once Available)
Once the `/api/Book` POST endpoint is fixed:
```bash
# This script adds test books through the API
python add_test_data_auth.py
```

### Option 4: Direct Database Access (If Available)
Connect to the database directly and insert test book records.

## Verification Steps

### Check if books exist:
```bash
python check_database.py
```

### Expected output:
```
✅ Books - 5 items
✅ Categories - 5 items
```

### Test if ready:
```bash
# Run just one shopping card test
pytest tests/test_shopping_cart.py::TestShoppingCart::test_add_to_cart -v
```

Should output:
- ✅ PASSED (if books exist)
- ⊘ SKIPPED (if no books - this is normal)

## Test Execution After Setup

### Run all tests:
```bash
pytest tests/ -v
```

### Run only authentication tests (work now):
```bash
pytest tests/test_authentication.py -v
```

### Run tests with product data required:
```bash
pytest tests/test_shopping_cart.py tests/test_product_search.py -v
```

## Current Test Results

- **Authentication**: ✅ 6 passing
- **Product Search**: SKIPPED (no books)
- **Shopping Cart**: SKIPPED (no books)
- **Checkout**: SKIPPED (no books)
- **Visual Tests**: ⊘ 10 passing

## Next Steps

1. **Choose one solution above** based on your access level
2. **Add 3-5 sample books** with titles, authors, and prices
3. **Run** `python check_database.py` to verify
4. **Execute tests** - they should now run properly
5. **Come back if** you hit auth issues with the API

## API Endpoints Reference

From `/swagger/v1/swagger.json`:

```
GET    /api/Book                           - Get all books
POST   /api/Book                           - Create book (needs auth)
GET    /api/Book/{id}                      - Get book detail
POST   /api/Login                          - Login user
POST   /api/User                           - Register user
GET    /api/Book/GetCategoriesList         - Get categories
```

## Questions?

- 🤔 Can't find admin panel? Check navigation menus
- 🔐 Need admin credentials? Check with your team
- 🗄️ Don't have database access? Use the UI approach
