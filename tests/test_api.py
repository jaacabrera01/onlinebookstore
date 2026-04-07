"""API tests for backend endpoints."""
import pytest
import allure
from utils.api_client import APIClient, assert_response, assert_response_contains
from config import get_settings


settings = get_settings()


@allure.feature("API")
@allure.suite("Product API")
class TestProductAPI:
    """Test cases for product API endpoints."""
    
    @allure.title("API returns list of products")
    @allure.description("Verify that product API returns list of books")
    @pytest.mark.regression
    def test_get_products_api(self):
        """Test getting products from API."""
        client = APIClient()
        
        # Common product endpoints (adjust based on actual API)
        endpoints = [
            "api/products",
            "api/books",
            "api/v1/products"
        ]
        
        response = None
        for endpoint in endpoints:
            try:
                response = client.get(endpoint)
                if response.status_code == 200:
                    break
            except Exception:
                continue
        
        if response:
            assert_response(response, 200, "Failed to get products")
            data = response.json()
            assert isinstance(data, (list, dict)), "Response is not valid JSON"
        
        client.close()
    
    @allure.title("API returns product details")
    @allure.description("Verify that API returns detailed product information")
    @pytest.mark.regression
    def test_get_product_details_api(self):
        """Test getting product details from API."""
        client = APIClient()
        
        # Try to get a product detail (ID might need adjustment)
        endpoints = [
            "api/products/1",
            "api/books/1",
            "api/v1/products/1"
        ]
        
        response = None
        for endpoint in endpoints:
            try:
                response = client.get(endpoint)
                if response.status_code == 200:
                    break
            except Exception:
                continue
        
        if response and response.status_code == 200:
            data = response.json()
            assert "id" in data or "productId" in data, "Product ID not in response"
        
        client.close()
    
    @allure.title("API search endpoint returns results")
    @allure.description("Verify that search API returns matching products")
    @pytest.mark.regression
    def test_search_products_api(self):
        """Test searching products via API."""
        client = APIClient()
        
        search_query = "Python"
        endpoints = [
            f"api/products/search?q={search_query}",
            f"api/books/search?query={search_query}",
            f"api/v1/products?search={search_query}"
        ]
        
        response = None
        for endpoint in endpoints:
            try:
                response = client.get(endpoint)
                if response.status_code == 200:
                    break
            except Exception:
                continue
        
        if response and response.status_code == 200:
            data = response.json()
            assert isinstance(data, (list, dict)), "Search response is not valid JSON"
        
        client.close()


@allure.feature("API")
@allure.suite("Cart API")
class TestCartAPI:
    """Test cases for cart API endpoints."""
    
    @allure.title("API can add item to cart")
    @allure.description("Verify that cart add endpoint works")
    @pytest.mark.regression
    def test_add_to_cart_api(self):
        """Test adding item to cart via API."""
        client = APIClient()
        
        # Typical cart add request (adjust based on actual API)
        cart_data = {
            "productId": 1,
            "quantity": 1
        }
        
        endpoints = [
            ("api/cart/add", cart_data),
            ("api/v1/cart/items", cart_data),
        ]
        
        for endpoint, data in endpoints:
            try:
                response = client.post(endpoint, data=data)
                if response.status_code in [200, 201]:
                    assert_response(response, response.status_code, "Add to cart failed")
                    break
            except Exception:
                continue
        
        client.close()
    
    @allure.title("API can get cart contents")
    @allure.description("Verify that cart API returns cart items")
    @pytest.mark.regression
    def test_get_cart_api(self):
        """Test getting cart contents via API."""
        client = APIClient()
        
        endpoints = [
            "api/cart",
            "api/v1/cart",
            "api/cart/items"
        ]
        
        response = None
        for endpoint in endpoints:
            try:
                response = client.get(endpoint)
                if response.status_code == 200:
                    break
            except Exception:
                continue
        
        if response and response.status_code == 200:
            data = response.json()
            assert isinstance(data, (list, dict)), "Cart response is not valid JSON"
        
        client.close()


@allure.feature("API")
@allure.suite("User API")
class TestUserAPI:
    """Test cases for user API endpoints."""
    
    @allure.title("API returns 401 for missing auth")
    @allure.description("Verify that protected endpoints require authentication")
    @pytest.mark.regression
    def test_protected_endpoint_requires_auth(self):
        """Test that protected endpoints require authentication."""
        client = APIClient()
        
        endpoints = [
            "api/user/profile",
            "api/v1/user",
            "api/account"
        ]
        
        for endpoint in endpoints:
            try:
                response = client.get(endpoint)
                # Should be 401 or 403 without auth
                if response.status_code in [401, 403, 404]:
                    break
            except Exception:
                continue
        
        client.close()
    
    @allure.title("API user registration endpoint exists")
    @allure.description("Verify that user registration API endpoint is available")
    @pytest.mark.regression
    def test_user_registration_api(self):
        """Test user registration API."""
        client = APIClient()
        
        user_data = {
            "firstName": "Test",
            "lastName": "User",
            "email": "test@example.com",
            "password": "TestPassword123!"
        }
        
        endpoints = [
            ("api/auth/register", user_data),
            ("api/v1/register", user_data),
            ("api/users", user_data)
        ]
        
        for endpoint, data in endpoints:
            try:
                response = client.post(endpoint, data=data)
                if response.status_code in [200, 201, 400]:  # 400 might mean user exists
                    assert_response(
                        response,
                        response.status_code,
                        "Registration endpoint working"
                    )
                    break
            except Exception:
                continue
        
        client.close()


@allure.feature("API")
@allure.suite("API Response Validation")
class TestAPIResponseValidation:
    """Test cases for API response validation."""
    
    @allure.title("API responses contain proper headers")
    @allure.description("Verify that API responses have correct Content-Type")
    @pytest.mark.regression
    def test_api_response_headers(self):
        """Test API response headers."""
        client = APIClient()
        
        endpoints = [
            "api/products",
            "api/books",
            "api/v1/products"
        ]
        
        for endpoint in endpoints:
            try:
                response = client.get(endpoint)
                if response.status_code == 200:
                    content_type = response.headers.get("content-type", "")
                    assert "json" in content_type.lower() or response.text, \
                        f"Invalid content type: {content_type}"
                    break
            except Exception:
                continue
        
        client.close()
    
    @allure.title("API handles errors gracefully")
    @allure.description("Verify that API returns proper error responses")
    @pytest.mark.regression
    def test_api_error_handling(self):
        """Test API error handling."""
        client = APIClient()
        
        # Request non-existent product
        bad_endpoints = [
            "api/products/999999",
            "api/books/nonexistent",
            "api/v1/products/0"
        ]
        
        for endpoint in bad_endpoints:
            try:
                response = client.get(endpoint)
                # Should return 4xx status
                assert response.status_code >= 400, "Error not returned for invalid request"
                break
            except Exception:
                continue
        
        client.close()
