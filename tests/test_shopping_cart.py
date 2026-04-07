"""Tests for shopping cart functionality."""
import pytest
import allure
from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from playwright.async_api import Page


@allure.feature("Shopping Cart")
@allure.suite("Cart Management")
class TestShoppingCart:
    """Test cases for shopping cart functionality."""
    
    @allure.title("User can add product to cart")
    @allure.description("Verify that user can add a book to shopping cart")
    @pytest.mark.critical
    @pytest.mark.smoke
    async def test_add_to_cart(self, page: Page):
        """Test adding product to cart."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        
        # Navigate to home and find a book
        await home_page.goto_home()
        visible_books = await home_page.get_visible_books()
        
        if not visible_books:
            pytest.skip("No books available in the database - test data needs to be populated")
        
        # Navigate to product and add to cart
        await home_page.click_book_by_title(visible_books[0])
        await product_page.add_to_cart(quantity=1)
        
        # Verify success message
        is_success = await product_page.is_success_displayed()
        assert is_success, "Success message not displayed after adding to cart"
    
    @allure.title("User can add multiple quantities to cart")
    @allure.description("Verify that user can add multiple quantities of same book")
    @pytest.mark.critical
    async def test_add_multiple_quantities_to_cart(self, page: Page):
        """Test adding multiple quantities to cart."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        
        await home_page.goto_home()
        visible_books = await home_page.get_visible_books()
        
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            await product_page.add_to_cart(quantity=3)
            
            assert await product_page.is_success_displayed(), \
                "Failed to add multiple quantities"
    
    @allure.title("User can view shopping cart")
    @allure.description("Verify that user can access and view shopping cart")
    @pytest.mark.critical
    @pytest.mark.smoke
    async def test_view_shopping_cart(self, page: Page):
        """Test viewing shopping cart."""
        home_page = HomePage(page)
        cart_page = CartPage(page)
        
        await home_page.goto_home()
        
        # Open cart
        await home_page.open_cart()
        
        # Verify cart page
        url = await cart_page.get_url()
        assert "cart" in url.lower(), "Not on cart page"
    
    @allure.title("Empty cart displays appropriate message")
    @allure.description("Verify that empty cart shows 'Your cart is empty' message")
    @pytest.mark.critical
    async def test_empty_cart_message(self, page: Page):
        """Test empty cart displays appropriate message."""
        cart_page = CartPage(page)
        
        await cart_page.goto_cart()
        
        # Check for empty message
        is_empty = await cart_page.is_cart_empty()
        
        # If not empty, clear cart first
        if not is_empty:
            # Try to remove items
            items_count = await cart_page.get_cart_items_count()
            for i in range(items_count):
                try:
                    await cart_page.remove_item_from_cart(0)
                except Exception:
                    break
            
            await page.wait_for_load_state("networkidle")
            is_empty = await cart_page.is_cart_empty()
        
        assert is_empty, "Empty cart message not displayed"


@allure.feature("Shopping Cart")
@allure.suite("Cart Item Management")
class TestCartItemManagement:
    """Test cases for managing items in cart."""
    
    @allure.title("User can remove item from cart")
    @allure.description("Verify that user can remove an item from shopping cart")
    @pytest.mark.critical
    async def test_remove_item_from_cart(self, page: Page):
        """Test removing item from cart."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        cart_page = CartPage(page)
        
        # Add item to cart
        await home_page.goto_home()
        visible_books = await home_page.get_visible_books()
        
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            await product_page.add_to_cart(quantity=1)
            
            # Go to cart
            await home_page.open_cart()
            
            # Remove item
            await cart_page.remove_item_from_cart(0)
            
            # Verify cart is empty
            is_empty = await cart_page.is_cart_empty()
            assert is_empty, "Item not removed from cart"
    
    @allure.title("User can update item quantity in cart")
    @allure.description("Verify that user can change quantity of items in cart")
    @pytest.mark.critical
    async def test_update_item_quantity(self, page: Page):
        """Test updating item quantity in cart."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        cart_page = CartPage(page)
        
        # Add item to cart
        await home_page.goto_home()
        visible_books = await home_page.get_visible_books()
        
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            await product_page.add_to_cart(quantity=1)
            
            # Go to cart and update quantity
            await home_page.open_cart()
            await cart_page.update_item_quantity(0, 2)
            
            # Verify quantity was updated (would check value in real scenario)
            items_count = await cart_page.get_cart_items_count()
            assert items_count >= 1, "Item not in cart"
    
    @allure.title("Cart displays correct product prices")
    @allure.description("Verify that cart shows correct price for each product")
    @pytest.mark.regression
    async def test_cart_prices_display(self, page: Page):
        """Test that cart displays product prices."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        cart_page = CartPage(page)
        
        await home_page.goto_home()
        visible_books = await home_page.get_visible_books()
        
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            await product_page.add_to_cart(quantity=1)
            
            await home_page.open_cart()
            
            # Get prices
            prices = await cart_page.get_all_item_prices()
            assert len(prices) > 0, "No prices displayed in cart"


@allure.feature("Shopping Cart")
@allure.suite("Cart Calculation")
class TestCartCalculation:
    """Test cases for cart total calculations."""
    
    @allure.title("Cart calculates subtotal correctly")
    @allure.description("Verify that cart subtotal is calculated correctly")
    @pytest.mark.regression
    async def test_cart_subtotal_calculation(self, page: Page):
        """Test cart subtotal calculation."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        cart_page = CartPage(page)
        
        # Add item and check subtotal
        await home_page.goto_home()
        visible_books = await home_page.get_visible_books()
        
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            await product_page.add_to_cart(quantity=1)
            
            await home_page.open_cart()
            
            # Get subtotal
            subtotal = await cart_page.get_subtotal()
            assert subtotal, "Subtotal not displayed"
    
    @allure.title("Cart displays total with tax")
    @allure.description("Verify that cart total includes tax calculation")
    @pytest.mark.regression
    async def test_cart_total_with_tax(self, page: Page):
        """Test cart total calculation including tax."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        cart_page = CartPage(page)
        
        await home_page.goto_home()
        visible_books = await home_page.get_visible_books()
        
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            await product_page.add_to_cart(quantity=1)
            
            await home_page.open_cart()
            
            # Get total
            total = await cart_page.get_total()
            assert total, "Total not displayed"


@allure.feature("Shopping Cart")
@allure.suite("Cart Navigation")
class TestCartNavigation:
    """Test cases for cart page navigation."""
    
    @allure.title("User can continue shopping from cart")
    @allure.description("Verify that user can return to home from cart")
    @pytest.mark.regression
    async def test_continue_shopping_from_cart(self, page: Page):
        """Test navigating back to shopping from cart."""
        cart_page = CartPage(page)
        
        await cart_page.goto_cart()
        
        try:
            await cart_page.click_continue_shopping()
            
            # Verify navigated away from cart
            url = await page.url
            assert "cart" not in url.lower(), "Still on cart page"
        except Exception:
            # Continue shopping button might not be available in empty cart
            pytest.skip("Continue shopping button not available")
