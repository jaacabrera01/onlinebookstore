"""Product detail page object."""
from pages import BasePage


class ProductDetailPage(BasePage):
    """Product detail page object model."""
    
    # Selectors
    PRODUCT_TITLE = 'h1.product-title'
    PRODUCT_AUTHOR = '.product-author'
    PRODUCT_PRICE = '.product-price'
    PRODUCT_RATING = '.product-rating'
    PRODUCT_DESCRIPTION = '.product-description'
    PRODUCT_IMAGE = '.product-image'
    QUANTITY_INPUT = '#quantity, input[type="number"]'
    ADD_TO_CART_BUTTON = 'button:has-text("Add to Cart")'
    WISHLIST_BUTTON = 'button:has-text("Add to Wishlist")'
    SUCCESS_MESSAGE = '.alert-success'
    ERROR_MESSAGE = '.alert-danger'
    BACK_BUTTON = 'a:has-text("Back")'
    RELATED_PRODUCTS = '.related-products .product-item'
    REVIEW_SECTION = '.reviews'
    CUSTOMER_REVIEWS = '.review-item'
    
    async def goto_product(self, product_id: str):
        """Navigate to product detail page."""
        await self.goto(f"book-details/{product_id}")
    
    async def get_product_title(self) -> str:
        """Get product title."""
        return await self.get_text(self.PRODUCT_TITLE)
    
    async def get_product_author(self) -> str:
        """Get product author."""
        return await self.get_text(self.PRODUCT_AUTHOR)
    
    async def get_product_price(self) -> str:
        """Get product price."""
        return await self.get_text(self.PRODUCT_PRICE)
    
    async def get_product_rating(self) -> str:
        """Get product rating."""
        return await self.get_text(self.PRODUCT_RATING)
    
    async def get_product_description(self) -> str:
        """Get product description."""
        return await self.get_text(self.PRODUCT_DESCRIPTION)
    
    async def set_quantity(self, quantity: int):
        """Set product quantity."""
        await self.fill(self.QUANTITY_INPUT, str(quantity))
    
    async def click_add_to_cart(self):
        """Click add to cart button."""
        await self.click(self.ADD_TO_CART_BUTTON)
    
    async def add_to_cart(self, quantity: int = 1):
        """Add product to cart with specified quantity."""
        await self.set_quantity(quantity)
        await self.click_add_to_cart()
        await self.page.wait_for_load_state("networkidle")
    
    async def click_add_to_wishlist(self):
        """Click add to wishlist button."""
        await self.click(self.WISHLIST_BUTTON)
    
    async def get_success_message(self) -> str:
        """Get success message."""
        return await self.get_text(self.SUCCESS_MESSAGE)
    
    async def is_success_displayed(self) -> bool:
        """Check if success message is displayed."""
        return await self.is_visible(self.SUCCESS_MESSAGE, timeout=5000)
    
    async def get_error_message(self) -> str:
        """Get error message."""
        return await self.get_text(self.ERROR_MESSAGE)
    
    async def is_error_displayed(self) -> bool:
        """Check if error message is displayed."""
        return await self.is_visible(self.ERROR_MESSAGE, timeout=5000)
    
    async def is_product_image_visible(self) -> bool:
        """Check if product image is visible."""
        return await self.is_visible(self.PRODUCT_IMAGE)
    
    async def get_related_products_count(self) -> int:
        """Get count of related products."""
        products = self.page.locator(self.RELATED_PRODUCTS)
        return await products.count()
    
    async def get_customer_review_count(self) -> int:
        """Get count of customer reviews."""
        reviews = self.page.locator(self.CUSTOMER_REVIEWS)
        return await reviews.count()
    
    async def click_back(self):
        """Click back button."""
        await self.click(self.BACK_BUTTON)
        await self.page.wait_for_load_state("networkidle")
