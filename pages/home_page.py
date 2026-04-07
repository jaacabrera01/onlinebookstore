"""Home page object."""
from pages import BasePage


class HomePage(BasePage):
    """Home page object model."""
    
    # Selectors
    SEARCH_INPUT = 'input[placeholder="Search books or authors"]'
    FEATURED_BOOKS = '[class*="item"], [class*="book"], [class*="product"]'
    CATEGORY_DROPDOWN = '//*[@id="categorySelect"]'
    SHOPPING_CART_BUTTON = 'a[href*="cart"], button:has-text("Cart")'
    USER_PROFILE_ICON = '[data-test-id="user-profile"], .user-icon'
    LOGOUT_BUTTON = 'button:has-text("Logout"), a:has-text("Logout")'
    LOGIN_LINK = 'a:has-text("Login"), button:has-text("Sign In")'
    BOOK_TITLE = '.book-title'
    BOOK_PRICE = '.book-price'
    BOOK_RATING = '.book-rating'
    ADD_TO_CART_BUTTON = 'button:has-text("Add to Cart")'
    
    async def goto_home(self):
        """Navigate to home page."""
        await self.goto("")
    
    async def search_for_book(self, query: str):
        """Search for a book."""
        # Ensure we're on home page and it's loaded
        await self.goto("")
        await self.page.wait_for_load_state("networkidle")
        
        # Fill search and press Enter
        await self.fill(self.SEARCH_INPUT, query)
        await self.page.press(self.SEARCH_INPUT, "Enter")
        await self.page.wait_for_load_state("networkidle")
    
    async def select_category(self, category: str):
        """Select category from dropdown."""
        await self.select_option(self.CATEGORY_DROPDOWN, category)
    
    async def get_featured_books_count(self) -> int:
        """Get count of featured books."""
        books = self.page.locator(self.FEATURED_BOOKS)
        return await books.count()
    
    async def click_book_by_title(self, title: str):
        """Click book by title."""
        # Find element containing the title text and click it
        book_element = self.page.locator(f'text="{title}"').first
        await book_element.click()
        await self.page.wait_for_load_state("networkidle")
    
    async def get_book_price(self, index: int = 0) -> str:
        """Get book price."""
        prices = self.page.locator(self.BOOK_PRICE)
        return await prices.nth(index).text_content() or ""
    
    async def click_login(self):
        """Click login link."""
        await self.click(self.LOGIN_LINK)
    
    async def click_logout(self):
        """Click logout button."""
        await self.click(self.USER_PROFILE_ICON)
        await self.page.wait_for_timeout(500)  # Brief wait for menu to open
        await self.click(self.LOGOUT_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def open_cart(self):
        """Open shopping cart."""
        await self.click(self.SHOPPING_CART_BUTTON)
        await self.page.wait_for_load_state("networkidle")
    
    async def is_user_logged_in(self) -> bool:
        """Check if user is logged in."""
        return await self.is_visible(self.USER_PROFILE_ICON, timeout=5000)
    
    async def get_visible_books(self) -> list:
        """Get all visible book titles on current page."""
        titles = await self.page.locator(self.BOOK_TITLE).all_text_contents()
        return [title.strip() for title in titles if title.strip()]
