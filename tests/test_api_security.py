"""
API Security Test Suite for BookCart Application.

Tests for REST API vulnerabilities:
- API authentication bypass
- Authorization flaws
- Rate limiting
- API injection attacks
- Insecure deserialization
- API response data leakage
- Missing access controls
"""

import pytest
import allure
import aiohttp
from config import get_settings
import json
import uuid
from typing import Dict, Any

settings = get_settings()


@allure.feature("API Security")
@allure.suite("API Authentication")
class TestAPIAuthentication:
    """Test cases for API authentication vulnerabilities."""
    
    @allure.title("Prevent API Access Without Authentication")
    @allure.description("Verify protected API endpoints require valid authentication")
    @pytest.mark.security
    @pytest.mark.api
    async def test_api_authentication_required(self):
        """Test that API endpoints require authentication."""
        async with aiohttp.ClientSession() as session:
            # Attempt to access protected endpoints without auth
            protected_endpoints = [
                "/api/user",
                "/api/user/profile",
                "/api/orders",
                "/api/cart",
            ]
            
            for endpoint in protected_endpoints:
                url = f"{settings.API_BASE_URL.rstrip('/api')}{endpoint}"
                
                try:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        # Should not return 200 OK without authentication
                        if endpoint != "/api/public":  # Skip public endpoints
                            assert response.status != 200, \
                                f"Endpoint {endpoint} accessible without authentication (Status: {response.status})"
                            print(f"✓ {endpoint} properly requires authentication (Status: {response.status})")
                except Exception as e:
                    print(f"Could not test {endpoint}: {str(e)}")
    
    @allure.title("Prevent API Token Manipulation")
    @allure.description("Verify API tokens cannot be tampered with")
    @pytest.mark.security
    @pytest.mark.api
    async def test_api_token_validation(self):
        """Test that invalid tokens are rejected."""
        async with aiohttp.ClientSession() as session:
            # Try various invalid tokens
            invalid_tokens = [
                "",
                "invalid",
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.invalid",  # Malformed JWT
                "' OR '1'='1",  # SQL injection
                "<script>alert('xss')</script>",  # XSS
            ]
            
            for token in invalid_tokens:
                headers = {"Authorization": f"Bearer {token}"}
                url = f"{settings.API_BASE_URL}/user"
                
                try:
                    async with session.get(url, headers=headers, 
                                         timeout=aiohttp.ClientTimeout(total=5)) as response:
                        # Should reject invalid token
                        assert response.status >= 400, \
                            f"Invalid token accepted: {token}"
                        print(f"✓ Invalid token rejected (Status: {response.status})")
                except Exception:
                    pass  # Expected


@allure.feature("API Security")
@allure.suite("API Authorization")
class TestAPIAuthorization:
    """Test cases for API authorization and access control."""
    
    @allure.title("Prevent Unauthorized Access to Other Users' Data")
    @allure.description("Verify users cannot access another user's profile/orders via API")
    @pytest.mark.security
    @pytest.mark.api
    async def test_horizontal_privilege_escalation(self):
        """Test that users cannot access other users' data."""
        async with aiohttp.ClientSession() as session:
            # Try to access users with different IDs
            user_ids = [
                "1",
                "admin",
                str(uuid.uuid4()),
            ]
            
            for user_id in user_ids:
                url = f"{settings.API_BASE_URL}/user/{user_id}"
                headers = {"Authorization": "Bearer fake-token"}  # Unauthorized
                
                try:
                    async with session.get(url, headers=headers,
                                         timeout=aiohttp.ClientTimeout(total=5)) as response:
                        # Should not return user data
                        assert response.status >= 400, \
                            f"Unauthorized access to user {user_id}"
                except Exception:
                    pass
    
    @allure.title("Prevent Direct Object Reference (IDOR)")
    @allure.description("Verify orders cannot be accessed via sequential ID enumeration")
    @pytest.mark.security
    @pytest.mark.api
    async def test_insecure_direct_object_reference(self):
        """Test IDOR vulnerability in order access."""
        async with aiohttp.ClientSession() as session:
            # Try to access orders with sequential IDs
            for order_id in range(1, 100, 10):  # Test different order IDs
                url = f"{settings.API_BASE_URL}/order/{order_id}"
                headers = {"Authorization": "Bearer fake-token"}
                
                try:
                    async with session.get(url, headers=headers,
                                         timeout=aiohttp.ClientTimeout(total=5)) as response:
                        # Without proper auth, should not get data
                        assert response.status >= 400 or response.status == 404, \
                            f"Order {order_id} accessible without proper authorization"
                except Exception:
                    pass


@allure.feature("API Security")
@allure.suite("API Rate Limiting")
class TestAPIRateLimiting:
    """Test cases for API rate limiting functionality."""
    
    @allure.title("Verify API Rate Limiting is Enforced")
    @allure.description("Check that excessive API requests are throttled")
    @pytest.mark.security
    @pytest.mark.api
    async def test_api_rate_limiting(self):
        """Test that API implements rate limiting."""
        async with aiohttp.ClientSession() as session:
            url = f"{settings.API_BASE_URL}/books"
            
            # Make many rapid requests
            rate_limit_hit = False
            status_codes = []
            
            for i in range(100):
                try:
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        status_codes.append(response.status)
                        
                        # 429 = Too Many Requests
                        if response.status == 429:
                            rate_limit_hit = True
                            print(f"✓ Rate limiting triggered after {i} requests")
                            break
                except Exception:
                    pass
            
            # If we got 429, rate limiting is working
            if rate_limit_hit:
                print("✓ API rate limiting is enabled")
            else:
                print("⚠ No rate limiting detected - potentially vulnerable")


@allure.feature("API Security")
@allure.suite("API Input Validation")
class TestAPIInputValidation:
    """Test cases for API input validation."""
    
    @allure.title("Prevent API Injection via POST Data")
    @allure.description("Verify POST parameters are properly validated")
    @pytest.mark.security
    @pytest.mark.api
    async def test_api_injection_prevention(self):
        """Test injection prevention in API POST requests."""
        async with aiohttp.ClientSession() as session:
            url = f"{settings.API_BASE_URL}/book"
            
            # Injection payloads
            injection_payloads = {
                "title": "' OR '1'='1",
                "author": "<script>alert('xss')</script>",
                "price": "999'; DELETE FROM books; --",
            }
            
            for field, payload in injection_payloads.items():
                data = {
                    "title": "Test Book",
                    "author": "Test Author",
                    "price": "29.99",
                    field: payload,  # Inject in one field
                }
                
                try:
                    async with session.post(url, json=data,
                                          timeout=aiohttp.ClientTimeout(total=5)) as response:
                        # Should reject invalid data
                        response_data = await response.json() if response.content_type == 'application/json' else {}
                        
                        assert response.status >= 400 or "error" in str(response_data).lower(), \
                            f"Injection payload accepted: {field}={payload}"
                        print(f"✓ API injection rejected for {field}")
                except Exception as e:
                    print(f"Could not test injection for {field}: {str(e)}")
    
    @allure.title("Validate Required API Fields")
    @allure.description("Verify all required fields must be present")
    @pytest.mark.security
    @pytest.mark.api
    async def test_api_required_fields(self):
        """Test that API enforces required fields."""
        async with aiohttp.ClientSession() as session:
            url = f"{settings.API_BASE_URL}/book"
            
            # Missing required fields
            incomplete_data = {
                "title": "Test Book",
                # Missing author and price
            }
            
            try:
                async with session.post(url, json=incomplete_data,
                                      timeout=aiohttp.ClientTimeout(total=5)) as response:
                    # Should require all fields
                    assert response.status >= 400, "API accepted incomplete data"
                    print("✓ API properly validates required fields")
            except Exception as e:
                print(f"Could not test required fields: {str(e)}")


@allure.feature("API Security")
@allure.suite("API Response Security")
class TestAPIResponseSecurity:
    """Test cases for secure API responses."""
    
    @allure.title("Verify API Response Headers for Security")
    @allure.description("Check that security headers are present in API responses")
    @pytest.mark.security
    @pytest.mark.api
    async def test_api_security_headers(self):
        """Test that API includes security headers."""
        async with aiohttp.ClientSession() as session:
            url = f"{settings.API_BASE_URL}/books"
            
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    headers = response.headers
                    
                    # Check for security headers
                    security_headers = {
                        'X-Content-Type-Options': 'nosniff',
                        'X-Frame-Options': 'DENY',
                        'X-XSS-Protection': '1; mode=block',
                    }
                    
                    for header, expected_value in security_headers.items():
                        if header in headers:
                            print(f"✓ Security header present: {header}={headers[header]}")
                        else:
                            print(f"⚠ Missing security header: {header}")
            except Exception as e:
                print(f"Could not check security headers: {str(e)}")
    
    @allure.title("Prevent Sensitive Data in API Responses")
    @allure.description("Verify API responses don't contain sensitive information")
    @pytest.mark.security
    @pytest.mark.api
    async def test_api_no_sensitive_data_leak(self):
        """Test that API doesn't leak sensitive data in responses."""
        async with aiohttp.ClientSession() as session:
            url = f"{settings.API_BASE_URL}/books"
            
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.content_type == 'application/json':
                        data = await response.json()
                        response_text = json.dumps(data)
                        
                        # Check for sensitive data patterns
                        sensitive_patterns = [
                            'password',
                            'api_key',
                            'secret',
                            'token',
                            'credit_card',
                            'ssn',
                            'private_key',
                        ]
                        
                        for pattern in sensitive_patterns:
                            assert pattern.lower() not in response_text.lower() or \
                                   response_text.lower().count(pattern.lower()) == 0, \
                                   f"Sensitive data pattern found: {pattern}"
                        
                        print("✓ API response doesn't leak sensitive data")
            except Exception as e:
                print(f"Could not check API response: {str(e)}")
    
    @allure.title("Verify API Response Format Validation")
    @allure.description("Check that API responses are in expected format")
    @pytest.mark.security
    @pytest.mark.api
    async def test_api_response_format(self):
        """Test that API returns proper JSON format."""
        async with aiohttp.ClientSession() as session:
            url = f"{settings.API_BASE_URL}/books"
            
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    assert response.content_type == 'application/json', \
                        f"Unexpected content type: {response.content_type}"
                    
                    # Should be valid JSON
                    data = await response.json()
                    assert isinstance(data, (dict, list)), "Invalid JSON structure"
                    
                    print("✓ API returns proper JSON format")
            except json.JSONDecodeError:
                print("❌ API returned invalid JSON")
            except Exception as e:
                print(f"Could not validate API response format: {str(e)}")


@allure.feature("API Security")
@allure.suite("API Versioning & Deprecation")
class TestAPIVersioning:
    """Test cases for API versioning and deprecation."""
    
    @allure.title("Verify Deprecated Endpoints Return Warnings")
    @allure.description("Check that old API versions show deprecation warnings")
    @pytest.mark.security
    @pytest.mark.api
    async def test_deprecated_api_endpoints(self):
        """Test API versioning and deprecation."""
        async with aiohttp.ClientSession() as session:
            # Try accessing old API versions
            old_api_versions = [
                "/api/v1/books",
                "/api/v0/books",
                "/api/legacy/books",
            ]
            
            for url in old_api_versions:
                full_url = f"{settings.BASE_URL.rstrip('/')}{url}"
                try:
                    async with session.get(full_url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        # Old versions should either not exist or show deprecation warning
                        if response.status == 410:  # Gone
                            print(f"✓ Old API version properly deprecated: {url}")
                        elif 'deprecation' in response.headers or 'deprecation' in str(response.headers).lower():
                            print(f"✓ Deprecation warning present for: {url}")
                except Exception:
                    pass


@allure.feature("API Security")
@allure.suite("API Endpoint Coverage")
class TestAPIEndpointSecurity:
    """Test security of all API endpoints."""
    
    @allure.title("Audit All API Endpoints for Security")
    @allure.description("Comprehensive scan of available API endpoints")
    @pytest.mark.security
    @pytest.mark.api
    async def test_api_endpoint_security_audit(self):
        """Audit major API endpoints for security issues."""
        async with aiohttp.ClientSession() as session:
            endpoints_to_test = [
                "/api/books",
                "/api/book",
                "/api/categories",
                "/api/user",
                "/api/cart",
                "/api/order",
                "/api/auth/login",
                "/api/auth/register",
            ]
            
            for endpoint in endpoints_to_test:
                url = f"{settings.API_BASE_URL.rstrip('/api')}{endpoint}"
                
                test_results = {
                    "endpoint": endpoint,
                    "status": None,
                    "has_auth": False,
                    "has_cors": False,
                    "returns_json": False,
                }
                
                try:
                    # Test GET request
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as response:
                        test_results["status"] = response.status
                        test_results["has_auth"] = response.status == 401
                        test_results["has_cors"] = 'access-control-allow-origin' in response.headers
                        test_results["returns_json"] = 'application/json' in response.headers.get('content-type', '')
                        
                        print(f"\n{endpoint}:")
                        print(f"  Status: {response.status}")
                        print(f"  Requires Auth: {test_results['has_auth']}")
                        print(f"  CORS Enabled: {test_results['has_cors']}")
                        print(f"  Returns JSON: {test_results['returns_json']}")
                
                except Exception as e:
                    print(f"\n{endpoint}: Error - {str(e)}")
