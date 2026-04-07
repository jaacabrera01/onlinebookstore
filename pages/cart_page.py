"""Shopping cart page object."""
from pages import BasePage


class CartPage(BasePage):
    """Shopping cart page object model."""
    
    # Selectors
    CART_ITEMS = '.cart-item'
    ITEM_TITLE = '.item-title'
    ITEM_PRICE = '.item-price'
    ITEM_QUANTITY = 'input[type="number"]'
    REMOVE_BUTTON = 'button:has-text("Remove")'
    UPDATE_BUTTON = 'button:has-text("Update")'
    CONTINUE_SHOPPING_BUTTON = 'a:has-text("Continue Shopping")'
    CHECKOUT_BUTTON = 'button:has-text("Checkout"), button:has-text("Proceed to Checkout")'
    SUBTOTAL = '.subtotal'
    TAX = '.tax'
    TOTAL = '.cart-total, .total-price'
    EMPTY_CART_MESSAGE = 'text=Your cart is empty'
    COUPON_INPUT = 'input[placeholder="Enter Coupon Code"]'
    APPLY_COUPON_BUTTON = 'button:has-text("Apply")'
    DISCOUNT = '.discount'
    
    async def goto_cart(self):
        """Navigate to cart page."""
        await self.goto("cart")
    
    async def get_cart_items_count(self) -> int:
        """Get count of items in cart."""
        items = self.page.locator(self.CART_ITEMS)
        return await items.count()
    
    async def get_item_titles(self) -> list:
        """Get all item titles in cart."""
        titles = await self.page.locator(self.ITEM_TITLE).all_text_contents()
        return [title.strip() for title in titles if title.strip()]
    
    async def update_item_quantity(self, item_index: int, quantity: int):
        """Update quantity of item in cart."""
        quantity_inputs = self.page.locator(self.ITEM_QUANTITY)
        await quantity_inputs.nth(item_index).fill(str(quantity))
        await self.click(self.UPDATE_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def remove_item_from_cart(self, item_index: int):
        """Remove item from cart."""
        remove_buttons = self.page.locator(self.REMOVE_BUTTON)
        await remove_buttons.nth(item_index).click()
        await self.page.wait_for_load_state("networkidle")
    
    async def get_subtotal(self) -> str:
        """Get cart subtotal."""
        return await self.get_text(self.SUBTOTAL)
    
    async def get_tax(self) -> str:
        """Get tax amount."""
        return await self.get_text(self.TAX)
    
    async def get_total(self) -> str:
        """Get cart total."""
        return await self.get_text(self.TOTAL)
    
    async def click_continue_shopping(self):
        """Click continue shopping button."""
        await self.click(self.CONTINUE_SHOPPING_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def click_checkout(self):
        """Click checkout button."""
        await self.click(self.CHECKOUT_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def is_cart_empty(self) -> bool:
        """Check if cart is empty."""
        return await self.is_visible(self.EMPTY_CART_MESSAGE, timeout=5000)
    
    async def apply_coupon(self, coupon_code: str):
        """Apply coupon code."""
        await self.fill(self.COUPON_INPUT, coupon_code)
        await self.click(self.APPLY_COUPON_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def get_discount_amount(self) -> str:
        """Get discount amount."""
        try:
            return await self.get_text(self.DISCOUNT)
        except Exception:
            return ""
    
    async def get_all_item_prices(self) -> list:
        """Get all item prices."""
        prices = await self.page.locator(self.ITEM_PRICE).all_text_contents()
        return [price.strip() for price in prices if price.strip()]
