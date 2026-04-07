"""Helper to add test data through API."""
import requests
import json
from typing import Dict, Any
from config import get_settings

settings = get_settings()


class TestDataHelper:
    """Helper to manage test data via API."""
    
    def __init__(self):
        self.base_url = settings.BASE_URL.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def add_test_book(self, 
                     title: str = "Test Book",
                     author: str = "Test Author",
                     price: float = 29.99,
                     category: str = "Fiction",
                     description: str = "A test book for automation testing",
                     image_url: str = "") -> Dict[str, Any]:
        """Add a test book to the database."""
        
        book_data = {
            "title": title,
            "author": author,
            "price": price,
            "categoryId": 1,  # Might need adjustment
            "description": description,
            "coverImage": image_url or "https://via.placeholder.com/300x400?text=Book+Cover"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/Book",
                json=book_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                book = response.json()
                print(f"✅ Book added: {title} (ID: {book.get('id', 'N/A')})")
                return book
            else:
                print(f"❌ Failed to add book: {response.status_code}")
                print(f"   Response: {response.text}")
                return {}
        except Exception as e:
            print(f"❌ Error adding book: {e}")
            return {}
    
    def get_all_books(self) -> list:
        """Get all books from the database."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/Book",
                timeout=10
            )
            
            if response.status_code == 200:
                books = response.json()
                print(f"✅ Found {len(books)} books in database")
                return books if isinstance(books, list) else [books]
            else:
                print(f"❌ Failed to get books: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error getting books: {e}")
            return []
    
    def add_sample_books(self, count: int = 5):
        """Add multiple sample books."""
        sample_books = [
            {"title": "Python Programming", "author": "John Smith", "price": 49.99, "category": "Programming"},
            {"title": "Web Development Guide", "author": "Jane Doe", "price": 39.99, "category": "Web"},
            {"title": "Database Design", "author": "Bob Johnson", "price": 59.99, "category": "Database"},
            {"title": "Cloud Computing", "author": "Alice Brown", "price": 44.99, "category": "Cloud"},
            {"title": "DevOps Handbook", "author": "Charlie Wilson", "price": 54.99, "category": "DevOps"},
        ]
        
        print(f"\n📚 Adding {min(count, len(sample_books))} sample books...")
        print("=" * 60)
        
        for book in sample_books[:count]:
            self.add_test_book(**book)
        
        print("=" * 60)
        books = self.get_all_books()
        return books


def main():
    """Main function to add test data."""
    helper = TestDataHelper()
    
    print("\n🔍 Checking current books...")
    current_books = helper.get_all_books()
    print(f"Database has {len(current_books)} books")
    
    if len(current_books) < 3:
        print("\n⚠️  Not enough books for testing!")
        print("Adding sample books...\n")
        helper.add_sample_books(5)
    else:
        print("✅ Database has enough books for testing")


if __name__ == "__main__":
    main()
