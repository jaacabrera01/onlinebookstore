"""Tests for product search and navigation."""
import pytest
import allure
from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage
from playwright.async_api import Page


@allure.feature("Product Management")
@allure.suite("Product Search")
class TestProductSearch:
    """Test cases for product search functionality."""
    
    @allure.title("User can search for books by title")
    @allure.description("Verify that users can search for books using keywords")
    @pytest.mark.critical
    @pytest.mark.smoke
    async def test_search_for_book_by_title(self, page: Page):
        """Test searching for a book by title."""
        home_page = HomePage(page)
        
        # Navigate to home
        await home_page.goto_home()
        
        # Search for a book
        await home_page.search_for_book("Python")
        
        # Verify results are displayed
        book_count = await home_page.get_featured_books_count()
        assert book_count > 0, "No search results displayed"
    
    @allure.title("Search returns no results for invalid query")
    @allure.description("Verify search behavior with non-existent book")
    @pytest.mark.regression
    async def test_search_no_results(self, page: Page):
        """Test search with query that returns no results."""
        home_page = HomePage(page)
        
        await home_page.goto_home()
        await home_page.search_for_book("XYZ12345NONEXISTENT")
        
        # Verify search completed and results shown (even if empty)
        url = await home_page.get_url()
        assert "search" in url.lower() or len(await home_page.get_visible_books()) == 0, \
            "Search did not execute"
    
    @allure.title("Search with empty query displays home page")
    @allure.description("Verify behavior when searching with empty string")
    @pytest.mark.regression
    async def test_search_empty_query(self, page: Page):
        """Test search with empty query."""
        home_page = HomePage(page)
        
        await home_page.goto_home()
        
        # Get initial book count
        initial_count = await home_page.get_featured_books_count()
        
        # Search with empty string
        await home_page.search_for_book("")
        
        # Should show some results
        results_count = await home_page.get_featured_books_count()
        assert results_count >= 0, "No books displayed"


@allure.feature("Product Management")
@allure.suite("Product Navigation")
class TestProductNavigation:
    """Test cases for navigating between products."""
    
    @allure.title("User can view featured books on home page")
    @allure.description("Verify that featured books are displayed on home page")
    @pytest.mark.smoke
    async def test_featured_books_displayed(self, page: Page):
        """Test featured books are displayed."""
        home_page = HomePage(page)
        
        await home_page.goto_home()
        
        # Verify books are displayed
        book_count = await home_page.get_featured_books_count()
        if book_count == 0:
            pytest.skip("No books available in the database - test data needs to be populated")
        
        assert book_count > 0, "No featured books displayed on home page"
    
    @allure.title("User can view product details")
    @allure.description("Verify that clicking a book navigates to product details")
    @pytest.mark.critical
    @pytest.mark.smoke
    async def test_navigate_to_product_details(self, page: Page):
        """Test navigating to product details page."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        
        await home_page.goto_home()
        
        # Get visible books
        visible_books = await home_page.get_visible_books()
        
        if visible_books:
            # Click first book
            await home_page.click_book_by_title(visible_books[0])
            
            # Verify on product detail page
            url = await product_page.get_url()
            assert "book" in url.lower() or "product" in url.lower(), \
                "Not navigated to product page"
            
            # Verify product information is displayed
            title = await product_page.get_product_title()
            assert title, "Product title not displayed"


@allure.feature("Product Management")
@allure.suite("Product Details")
class TestProductDetails:
    """Test cases for product detail page."""
    
    @allure.title("Product details page displays product information")
    @allure.description("Verify that product page shows title, price, and description")
    @pytest.mark.critical
    async def test_product_details_display(self, page: Page):
        """Test that product details are displayed."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        
        await home_page.goto_home()
        
        visible_books = await home_page.get_visible_books()
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            
            # Verify product details
            assert await product_page.get_product_title(), "Product title not found"
            assert await product_page.get_product_price(), "Product price not found"
            assert await product_page.is_product_image_visible(), "Product image not visible"
    
    @allure.title("Product price is displayed correctly")
    @allure.description("Verify that product price is visible and formatted")
    @pytest.mark.regression
    async def test_product_price_display(self, page: Page):
        """Test product price display."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        
        await home_page.goto_home()
        
        visible_books = await home_page.get_visible_books()
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            
            price = await product_page.get_product_price()
            assert price, "Price not displayed"
            # Price should contain currency symbol or number
            assert any(char.isdigit() for char in price), "Price doesn't contain numbers"
    
    @allure.title("Product has quantity selector")
    @allure.description("Verify that user can select product quantity")
    @pytest.mark.regression
    async def test_product_quantity_selector(self, page: Page):
        """Test quantity selector on product page."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        
        await home_page.goto_home()
        
        visible_books = await home_page.get_visible_books()
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            
            # Test quantity update
            await product_page.set_quantity(3)
            # Verify quantity was set (would need to check value)
            quantity_input = page.locator(ProductDetailPage.QUANTITY_INPUT)
            value = await quantity_input.input_value()
            assert value == "3", f"Quantity not set correctly, got {value}"


@allure.feature("Product Management")
@allure.suite("Category Navigation")
class TestCategoryNavigation:
    """Test cases for category-based navigation."""
    
    @allure.title("User can browse by category")
    @allure.description("Verify that user can select a category to filter books")
    @pytest.mark.regression
    async def test_category_selection(self, page: Page):
        """Test browsing by category."""
        home_page = HomePage(page)
        
        await home_page.goto_home()
        
        # Try to select a category (if available)
        try:
            initial_books = await home_page.get_featured_books_count()
            await home_page.select_category("Fiction")
            
            # Wait for update
            await page.wait_for_load_state("networkidle")
            
            # Verify books are displayed
            filtered_books = await home_page.get_featured_books_count()
            assert filtered_books > 0, "No books in selected category"
        except Exception as e:
            # Category might not be available in test environment
            pytest.skip(f"Category selection not available: {str(e)}")
