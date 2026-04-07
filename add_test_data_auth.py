"""Helper to add test data with authentication."""
import requests
import json
from config import get_settings

settings = get_settings()


class AuthenticatedTestDataHelper:
    """Helper to manage test data via API with authentication."""
    
    def __init__(self, username: str = settings.TEST_USERNAME, password: str = settings.TEST_PASSWORD):
        self.base_url = settings.BASE_URL.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.token = None
        self.user_id = None
        
        # Try to authenticate
        self.authenticate(username, password)
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate and get auth token."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/Login",
                json={"userName": username, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token")
                self.user_id = data.get("userId")
                
                if self.token:
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                    print(f"✅ Authenticated as {username}")
                    return True
                else:
                    print(f"❌ No token in response")
                    return False
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {e}")
            return False
    
    def add_test_book(self, 
                     title: str = "Test Book",
                     author: str = "Test Author",
                     price: float = 29.99,
                     description: str = "A test book") -> dict:
        """Add a test book to the database."""
        
        book_data = {
            "title": title,
            "author": author,
            "price": price,
            "description": description,
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/Book",
                json=book_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                book = response.json()
                print(f"✅ Book added: {title}")
                return book
            else:
                print(f"❌ Failed to add book: {response.status_code}")
                print(f"   Details: {response.text[:200]}")
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
                if isinstance(books, list):
                    print(f"✅ Found {len(books)} books")
                    return books
                else:
                    print(f"✅ Found books (non-list response)")
                    return [books] if books else []
            else:
                print(f"❌ Failed to get books: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error getting books: {e}")
            return []
    
    def add_sample_books(self, count: int = 5):
        """Add multiple sample books."""
        if not self.token:
            print("❌ Not authenticated. Cannot add books.")
            return []
        
        sample_books = [
            {"title": "Python Programming", "author": "John Smith", "price": 49.99},
            {"title": "Web Development Guide", "author": "Jane Doe", "price": 39.99},
            {"title": "Database Design", "author": "Bob Johnson", "price": 59.99},
            {"title": "Cloud Computing", "author": "Alice Brown", "price": 44.99},
            {"title": "DevOps Handbook", "author": "Charlie Wilson", "price": 54.99},
        ]
        
        print(f"\n📚 Adding {min(count, len(sample_books))} sample books...")
        print("=" * 60)
        
        for book in sample_books[:count]:
            self.add_test_book(**book)
        
        print("=" * 60)
        return self.get_all_books()


def main():
    """Main function to manage test data."""
    print("\n🔐 Authenticating with admin credentials...")
    helper = AuthenticatedTestDataHelper()
    
    if not helper.token:
        print("\n⚠️  Could not authenticate!")
        print("   Trying to fetch books without authentication...")
    
    print("\n📖 Checking current books...")
    books = helper.get_all_books()
    
    if len(books) < 3:
        if helper.token:
            print("\n⚠️  Not enough books for testing!")
            helper.add_sample_books(5)
        else:
            print("❌ Cannot add books without authentication")
            print("   Check your TEST_USERNAME and TEST_PASSWORD in config.py")
    else:
        print(f"✅ Database has {len(books)} books - ready for testing!")


if __name__ == "__main__":
    main()
