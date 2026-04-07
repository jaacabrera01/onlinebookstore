"""Checkout page object."""
from pages import BasePage


class CheckoutPage(BasePage):
    """Checkout page object model."""
    
    # Selectors - Billing Address
    FIRST_NAME_INPUT = 'input[placeholder*="First"]'
    LAST_NAME_INPUT = 'input[placeholder*="Last"]'
    EMAIL_INPUT = 'input[type="email"]'
    PHONE_INPUT = 'input[type="tel"]'
    ADDRESS_INPUT = 'input[placeholder*="Address"]'
    CITY_INPUT = 'input[placeholder*="City"]'
    STATE_SELECT = 'select[name*="state"]'
    ZIP_CODE_INPUT = 'input[placeholder*="Zip"], input[placeholder*="Postal"]'
    COUNTRY_SELECT = 'select[name*="country"]'
    
    # Shipping
    SHIPPING_METHOD_SELECT = 'select[name*="shipping"]'
    SAME_AS_BILLING_CHECKBOX = 'input[type="checkbox"][name*="same"]'
    
    # Payment
    CARD_NUMBER_INPUT = 'input[placeholder*="Card"], input[placeholder*="4242"]'
    CARD_EXPIRY_INPUT = 'input[placeholder*="MM/YY"], input[placeholder*="Expiry"]'
    CARD_CVV_INPUT = 'input[placeholder*="CVC"], input[placeholder*="CVV"]'
    CARDHOLDER_NAME_INPUT = 'input[placeholder*="Cardholder"]'
    
    # Payment Method
    CREDIT_CARD_RADIO = 'input[type="radio"][value="card"]'
    DEBIT_CARD_RADIO = 'input[type="radio"][value="debit"]'
    PAYMENT_METHOD_SECTION = '.payment-methods'
    
    # Actions
    PLACE_ORDER_BUTTON = 'button:has-text("Place Order"), button:has-text("Complete Purchase")'
    CANCEL_BUTTON = 'button:has-text("Cancel")'
    REVIEW_ORDER_SECTION = '.order-review, .order-summary'
    
    # Messages
    SUCCESS_MESSAGE = '.alert-success'
    ERROR_MESSAGE = '.alert-danger'
    ORDER_CONFIRMATION = '.order-confirmation, .confirmation-message'
    ORDER_NUMBER = '.order-number'
    
    async def goto_checkout(self):
        """Navigate to checkout page."""
        await self.goto("checkout")
    
    async def fill_billing_address(self, first_name: str, last_name: str, email: str, 
                                    phone: str, address: str, city: str, 
                                    state: str, zip_code: str, country: str = "US"):
        """Fill billing address form."""
        await self.fill(self.FIRST_NAME_INPUT, first_name)
        await self.fill(self.LAST_NAME_INPUT, last_name)
        await self.fill(self.EMAIL_INPUT, email)
        await self.fill(self.PHONE_INPUT, phone)
        await self.fill(self.ADDRESS_INPUT, address)
        await self.fill(self.CITY_INPUT, city)
        await self.select_option(self.STATE_SELECT, state)
        await self.fill(self.ZIP_CODE_INPUT, zip_code)
        await self.select_option(self.COUNTRY_SELECT, country)
    
    async def select_same_as_billing(self):
        """Select same as billing for shipping address."""
        await self.check_element(self.SAME_AS_BILLING_CHECKBOX)
    
    async def select_shipping_method(self, method: str):
        """Select shipping method."""
        await self.select_option(self.SHIPPING_METHOD_SELECT, method)
    
    async def fill_credit_card(self, card_number: str, expiry: str, cvv: str, cardholder_name: str):
        """Fill credit card information."""
        await self.click(self.CREDIT_CARD_RADIO)
        await self.fill(self.CARD_NUMBER_INPUT, card_number)
        await self.fill(self.CARD_EXPIRY_INPUT, expiry)
        await self.fill(self.CARD_CVV_INPUT, cvv)
        await self.fill(self.CARDHOLDER_NAME_INPUT, cardholder_name)
    
    async def complete_checkout(self, first_name: str, last_name: str, email: str,
                               phone: str, address: str, city: str, state: str,
                               zip_code: str, card_number: str, expiry: str,
                               cvv: str, cardholder_name: str):
        """Complete full checkout process."""
        # Fill billing address
        await self.fill_billing_address(
            first_name, last_name, email, phone, address, city, state, zip_code
        )
        
        # Select same as billing
        await self.select_same_as_billing()
        
        # Select shipping method
        await self.select_shipping_method("Standard")
        
        # Fill credit card
        await self.fill_credit_card(card_number, expiry, cvv, cardholder_name)
        
        # Place order
        await self.click_place_order()
    
    async def click_place_order(self):
        """Click place order button."""
        await self.click(self.PLACE_ORDER_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def is_order_confirmation_displayed(self) -> bool:
        """Check if order confirmation is displayed."""
        return await self.is_visible(self.ORDER_CONFIRMATION, timeout=10000)
    
    async def get_success_message(self) -> str:
        """Get success message."""
        return await self.get_text(self.SUCCESS_MESSAGE)
    
    async def get_error_message(self) -> str:
        """Get error message."""
        return await self.get_text(self.ERROR_MESSAGE)
    
    async def is_error_displayed(self) -> bool:
        """Check if error message is displayed."""
        return await self.is_visible(self.ERROR_MESSAGE, timeout=5000)
    
    async def get_order_number(self) -> str:
        """Get order number from confirmation."""
        try:
            return await self.get_text(self.ORDER_NUMBER)
        except Exception:
            return ""
    
    async def click_cancel(self):
        """Click cancel button."""
        await self.click(self.CANCEL_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def is_review_order_visible(self) -> bool:
        """Check if order review section is visible."""
        return await self.is_visible(self.REVIEW_ORDER_SECTION)
