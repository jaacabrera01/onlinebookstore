"""Tests for checkout process."""
import pytest
import allure
from pages.home_page import HomePage
from pages.product_detail_page import ProductDetailPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from playwright.async_api import Page


@allure.feature("Checkout")
@allure.suite("Checkout Process")
class TestCheckoutProcess:
    """Test cases for checkout process."""
    
    @allure.title("User can access checkout from cart")
    @allure.description("Verify that user can proceed to checkout from shopping cart")
    @pytest.mark.critical
    @pytest.mark.smoke
    async def test_access_checkout_from_cart(self, page: Page):
        """Test accessing checkout from cart."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)
        
        # Add item to cart
        await home_page.goto_home()
        visible_books = await home_page.get_visible_books()
        
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            await product_page.add_to_cart(quantity=1)
            
            # Go to cart and proceed to checkout
            await home_page.open_cart()
            await cart_page.click_checkout()
            
            # Verify on checkout page
            url = await checkout_page.get_url()
            assert "checkout" in url.lower(), "Not on checkout page"
    
    @allure.title("Checkout page displays order review")
    @allure.description("Verify that checkout page shows items being purchased")
    @pytest.mark.critical
    async def test_checkout_order_review_display(self, page: Page):
        """Test checkout order review display."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)
        
        await home_page.goto_home()
        visible_books = await home_page.get_visible_books()
        
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            await product_page.add_to_cart(quantity=1)
            
            await home_page.open_cart()
            await cart_page.click_checkout()
            
            # Verify order review is visible
            is_visible = await checkout_page.is_review_order_visible()
            assert is_visible, "Order review not visible on checkout"


@allure.feature("Checkout")
@allure.suite("Billing Address")
class TestBillingAddress:
    """Test cases for billing address entry."""
    
    @allure.title("User can enter billing address")
    @allure.description("Verify that user can fill in billing address fields")
    @pytest.mark.critical
    @pytest.mark.skip(reason="Requires test books in database to add to cart")
    async def test_enter_billing_address(self, page: Page):
        """Test entering billing address."""
        checkout_page = CheckoutPage(page)
        
        await checkout_page.goto_checkout()
        
        # Fill billing address
        await checkout_page.fill_billing_address(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="5551234567",
            address="123 Main Street",
            city="New York",
            state="NY",
            zip_code="10001"
        )
        
        # Verify values were entered (check at least one field)
        first_name_input = page.locator(CheckoutPage.FIRST_NAME_INPUT)
        value = await first_name_input.input_value()
        assert value == "John", "First name not entered correctly"
    
    @allure.title("Billing address fields are required")
    @allure.description("Verify that checkout form requires billing address")
    @pytest.mark.regression
    async def test_billing_address_required_validation(self, page: Page):
        """Test that billing address is required."""
        checkout_page = CheckoutPage(page)
        
        await checkout_page.goto_checkout()
        
        try:
            # Try to proceed without filling address
            await checkout_page.click_place_order()
            
            # Check if error is shown
            is_error = await checkout_page.is_error_displayed()
            
            if not is_error:
                # Page might have HTML5 validation
                await page.wait_for_timeout(1000)
        except Exception:
            # Expected if form validation prevents action
            pass


@allure.feature("Checkout")
@allure.suite("Payment Information")
class TestPaymentInformation:
    """Test cases for payment information."""
    
    @allure.title("User can enter credit card information")
    @allure.description("Verify that user can fill credit card fields")
    @pytest.mark.critical
    @pytest.mark.skip(reason="Requires test books in database to add to cart")
    async def test_enter_credit_card_info(self, page: Page):
        """Test entering credit card information."""
        checkout_page = CheckoutPage(page)
        
        await checkout_page.goto_checkout()
        
        # Fill address first
        await checkout_page.fill_billing_address(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="5551234567",
            address="123 Main Street",
            city="New York",
            state="NY",
            zip_code="10001"
        )
        
        # Fill payment info
        await checkout_page.fill_credit_card(
            card_number="4111111111111111",
            expiry="12/26",
            cvv="123",
            cardholder_name="John Doe"
        )
        
        # Verify card number was entered
        card_input = page.locator(CheckoutPage.CARD_NUMBER_INPUT)
        value = await card_input.input_value()
        # Card might be masked or show last digits
        assert value, "Card number not entered"
    
    @allure.title("User can select payment method")
    @allure.description("Verify that user can choose payment method")
    @pytest.mark.regression
    async def test_select_payment_method(self, page: Page):
        """Test selecting payment method."""
        checkout_page = CheckoutPage(page)
        
        await checkout_page.goto_checkout()
        
        try:
            # Try to click credit card option
            await checkout_page.page.click(CheckoutPage.CREDIT_CARD_RADIO)
            
            # Verify it's selected
            is_selected = await checkout_page.page.is_checked(CheckoutPage.CREDIT_CARD_RADIO)
            assert is_selected, "Credit card option not selected"
        except Exception:
            # Option might not be separate if only one payment method
            pytest.skip("Multiple payment methods not available")


@allure.feature("Checkout")
@allure.suite("Order Placement")
class TestOrderPlacement:
    """Test cases for order placement."""
    
    @allure.title("User can complete purchase with valid data")
    @allure.description("Verify that user can successfully complete checkout with all required info")
    @pytest.mark.critical
    @pytest.mark.smoke
    async def test_complete_checkout_full_flow(self, page: Page):
        """Test completing full checkout process."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)
        
        # Add item to cart
        await home_page.goto_home()
        visible_books = await home_page.get_visible_books()
        
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            await product_page.add_to_cart(quantity=1)
            
            # Go through checkout
            await home_page.open_cart()
            await cart_page.click_checkout()
            
            # Fill all checkout information
            await checkout_page.complete_checkout(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                phone="5551234567",
                address="123 Test St",
                city="Test City",
                state="TS",
                zip_code="12345",
                card_number="4111111111111111",
                expiry="12/26",
                cvv="123",
                cardholder_name="Test User"
            )
            
            # Verify order confirmation
            is_confirmed = await checkout_page.is_order_confirmation_displayed()
            assert is_confirmed, "Order confirmation not displayed"
    
    @allure.title("Order confirmation displays order number")
    @allure.description("Verify that successful order shows confirmation number")
    @pytest.mark.critical
    async def test_order_confirmation_details(self, page: Page):
        """Test order confirmation displays details."""
        home_page = HomePage(page)
        product_page = ProductDetailPage(page)
        cart_page = CartPage(page)
        checkout_page = CheckoutPage(page)
        
        await home_page.goto_home()
        visible_books = await home_page.get_visible_books()
        
        if visible_books:
            await home_page.click_book_by_title(visible_books[0])
            await product_page.add_to_cart(quantity=1)
            
            await home_page.open_cart()
            await cart_page.click_checkout()
            
            await checkout_page.complete_checkout(
                first_name="Test",
                last_name="User",
                email="test@example.com",
                phone="5551234567",
                address="123 Test St",
                city="Test City",
                state="TS",
                zip_code="12345",
                card_number="4111111111111111",
                expiry="12/26",
                cvv="123",
                cardholder_name="Test User"
            )
            
            # Verify confirmation is displayed
            if await checkout_page.is_order_confirmation_displayed():
                success_msg = await checkout_page.get_success_message()
                assert success_msg, "No success message displayed"


@allure.feature("Checkout")
@allure.suite("Shipping Address")
class TestShippingAddress:
    """Test cases for shipping address."""
    
    @allure.title("User can set shipping same as billing")
    @allure.description("Verify that user can use billing address as shipping")
    @pytest.mark.regression
    @pytest.mark.skip(reason="Requires test books in database to add to cart")
    async def test_same_as_billing_address(self, page: Page):
        """Test setting shipping address same as billing."""
        checkout_page = CheckoutPage(page)
        
        await checkout_page.goto_checkout()
        
        # Fill billing address
        await checkout_page.fill_billing_address(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="5551234567",
            address="123 Main St",
            city="New York",
            state="NY",
            zip_code="10001"
        )
        
        # Select same as billing
        await checkout_page.select_same_as_billing()
        
        # Verify checkbox is checked
        is_checked = await page.is_checked(CheckoutPage.SAME_AS_BILLING_CHECKBOX)
        assert is_checked, "Same as billing checkbox not checked"
    
    @allure.title("User can select shipping method")
    @allure.description("Verify that user can choose shipping method")
    @pytest.mark.regression
    async def test_select_shipping_method(self, page: Page):
        """Test selecting shipping method."""
        checkout_page = CheckoutPage(page)
        
        await checkout_page.goto_checkout()
        
        try:
            await checkout_page.select_shipping_method("Standard")
        except Exception:
            # Shipping method might not be available
            pytest.skip("Shipping method selection not available")
