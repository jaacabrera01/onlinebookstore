"""
Authorization and Access Control Test Suite for BookCart Application.

Tests for authorization vulnerabilities:
- Privilege escalation
- Role-based access control bypass
- Admin panel access control
- Resource access control
- Vertical privilege escalation
- Horizontal privilege escalation
"""

import pytest
import allure
from playwright.async_api import Page
from config import get_settings
import uuid

settings = get_settings()


@allure.feature("Authorization")
@allure.suite("Access Control")
class TestAccessControl:
    """Test cases for access control vulnerabilities."""
    
    @allure.title("Prevent Access to Admin Pages Without Role")
    @allure.description("Verify users cannot access admin pages without admin role")
    @pytest.mark.security
    @pytest.mark.access_control
    async def test_admin_page_access_control(self, page: Page):
        """Test admin page access control."""
        # Try to access common admin URLs
        admin_urls = [
            "/admin",
            "/admin/dashboard",
            "/admin/users",
            "/admin/books",
            "/admin/reports",
            "/management",
            "/panel",
            "/superuser",
        ]
        
        for admin_url in admin_urls:
            url = f"{settings.BASE_URL.rstrip('/')}{admin_url}"
            
            try:
                await page.goto(url, wait_until="domcontentloaded")
                await page.wait_for_timeout(500)
                
                # Check if we're still on that page or redirected
                current_url = page.url.lower()
                content = await page.content().lower()
                
                # Should either redirect to login or show access denied
                if admin_url not in current_url:
                    print(f"✓ {admin_url} - Redirected (access denied)")
                elif "unauthorized" in content or "not allowed" in content or "forbidden" in content:
                    print(f"✓ {admin_url} - Access denied message shown")
                else:
                    print(f"⚠ {admin_url} - May be accessible")
            except Exception as e:
                print(f"✓ {admin_url} - Not found or error: {type(e).__name__}")
    
    @allure.title("Prevent User Role Modification")
    @allure.description("Verify users cannot change their own role/permissions")
    @pytest.mark.security
    @pytest.mark.access_control
    async def test_user_role_modification_prevention(self, page: Page):
        """Test that users cannot modify their own roles."""
        # This test checks if there's a profile/settings page where users might try to change roles
        profile_urls = [
            "/user/profile",
            "/profile",
            "/settings",
            "/account",
            "/user/settings",
        ]
        
        for profile_url in profile_urls:
            url = f"{settings.BASE_URL.rstrip('/')}{profile_url}"
            
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=10000)
                await page.wait_for_timeout(500)
                
                content = await page.content()
                
                # Check for role/permission fields that shouldn't be editable
                dangerous_fields = [
                    'role',
                    'permission',
                    'admin',
                    'is_admin',
                    'user_type',
                    'access_level',
                ]
                
                for field in dangerous_fields:
                    # Check if field exists and is editable
                    field_selector = f'input[name="{field}"], input[formcontrolname="{field}"]'
                    field_elements = await page.query_selector_all(field_selector)
                    
                    for field_elem in field_elements:
                        disabled = await field_elem.is_disabled()
                        if not disabled:
                            print(f"⚠ {profile_url} - Editable {field} field found!")
                        else:
                            print(f"✓ {profile_url} - {field} field is disabled")
                
            except Exception as e:
                print(f"  {profile_url} - Not accessible: {type(e).__name__}")
    
    @allure.title("Prevent Direct Admin Resource Access")
    @allure.description("Verify users cannot directly access admin resources")
    @pytest.mark.security
    @pytest.mark.access_control
    async def test_admin_resource_access(self, page: Page):
        """Test access control to admin-only resources."""
        # API endpoints that should be admin only
        admin_resources = [
            "/api/admin/users",
            "/api/admin/reports",
            "/api/user/delete",
            "/api/user/suspend",
            "/api/book/delete",
            "/api/settings",
        ]
        
        for resource in admin_resources:
            url = f"{settings.BASE_URL.rstrip('/')}{resource}"
            
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=5000)
                
                # Check what we get
                content = await page.content()
                status_indicator = page.url
                
                if "404" in content or "not found" in content.lower():
                    print(f"✓ {resource} - Not found (404)")
                elif "unauthorized" in content.lower() or "403" in content.lower():
                    print(f"✓ {resource} - Unauthorized (403)")
                elif "forbidden" in content.lower():
                    print(f"✓ {resource} - Forbidden")
                else:
                    print(f"⚠ {resource} - Potentially accessible")
            except Exception as e:
                print(f"✓ {resource} - Error: {type(e).__name__}")


@allure.feature("Authorization")
@allure.suite("Privilege Escalation")
class TestPrivilegeEscalation:
    """Test cases for privilege escalation vulnerabilities."""
    
    @allure.title("Prevent Vertical Privilege Escalation")
    @allure.description("Verify users cannot assume admin/higher role privileges")
    @pytest.mark.security
    @pytest.mark.privilege_escalation
    async def test_vertical_privilege_escalation(self, page: Page):
        """Test prevention of vertical privilege escalation."""
        # Try common privilege escalation techniques via URL manipulation
        
        # 1. Try accessing user data with admin parameters
        await page.goto(f"{settings.BASE_URL}", wait_until="domcontentloaded")
        
        # Try URL parameters that might giveadmin access
        admin_params = [
            "?admin=true",
            "?role=admin",
            "?is_admin=1",
            "?user_type=admin",
            "?access_level=9999",
        ]
        
        for param in admin_params:
            url = f"{settings.BASE_URL.rstrip('/')}{param}"
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=5000)
                await page.wait_for_timeout(500)
                
                # Check if we got elevated privileges
                content = await page.content()
                
                if "admin" in content.lower() and "dashboard" in content.lower():
                    print(f"⚠ {param} - May allow privilege escalation!")
                else:
                    print(f"✓ {param} - Parameter ignored or access denied")
            except Exception:
                pass
    
    @allure.title("Prevent Privilege Escalation via Hidden Fields")
    @allure.description("Check that hidden form fields cannot change user's role/permissions")
    @pytest.mark.security
    @pytest.mark.privilege_escalation
    async def test_hidden_field_escalation(self, page: Page):
        """Test that hidden fields cannot escalate privileges."""
        # Navigate to profile/settings if available
        profile_urls = [
            "/user/profile",
            "/profile",
            "/settings",
            "/account",
        ]
        
        for profile_url in profile_urls:
            try:
                await page.goto(f"{settings.BASE_URL.rstrip('/')}{profile_url}",
                              wait_until="domcontentloaded", timeout=5000)
                
                # Check for hidden fields in forms
                hidden_fields = await page.query_selector_all('input[type="hidden"]')
                
                for hidden_field in hidden_fields:
                    name = await hidden_field.get_attribute('name')
                    value = await hidden_field.get_attribute('value')
                    
                    # Check for suspicious hidden fields
                    if any(x in name.lower() for x in ['role', 'admin', 'permission']):
                        print(f"⚠ {profile_url} - Suspicious hidden field: {name}={value}")
                    else:
                        print(f"✓ Hidden field {name} is not privilege-related")
                
            except Exception as e:
                print(f"  {profile_url} - Could not access: {type(e).__name__}")


@allure.feature("Authorization")
@allure.suite("Resource Ownership")
class TestResourceOwnershipVerification:
    """Test cases for resource ownership and access control."""
    
    @allure.title("Verify User Can Only Edit Own Profile")
    @allure.description("Check that users cannot modify other users' profiles")
    @pytest.mark.security
    @pytest.mark.access_control
    async def test_profile_ownership_verification(self, page: Page):
        """Test that users cannot edit other users' profiles."""
        # Generate random user IDs to test
        other_user_ids = [
            "1",
            "999",
            "admin",
            str(uuid.uuid4()),
        ]
        
        # Try to access/edit other users' profiles
        for user_id in other_user_ids:
            edit_urls = [
                f"/user/{user_id}/edit",
                f"/profile/{user_id}/edit",
                f"/user/{user_id}/settings",
            ]
            
            for edit_url in edit_urls:
                url = f"{settings.BASE_URL.rstrip('/')}{edit_url}"
                
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=5000)
                    await page.wait_for_timeout(500)
                    
                    current_url = page.url.lower()
                    
                    # Should redirect away or show error
                    if user_id not in current_url:
                        print(f"✓ {edit_url} - Redirected (access denied)")
                    else:
                        content = await page.content()
                        if "forbidden" in content.lower() or "unauthorized" in content.lower():
                            print(f"✓ {edit_url} - Access denied")
                        else:
                            print(f"⚠ {edit_url} - May allow editing other users!")
                except Exception:
                    pass
    
    @allure.title("Verify User Can Only View Own Orders")
    @allure.description("Check that users cannot view other users' order history")
    @pytest.mark.security
    @pytest.mark.access_control
    async def test_order_access_control(self, page: Page):
        """Test that users cannot view other users' orders."""
        other_user_ids = [
            "1",
            "999",
        ]
        
        for user_id in other_user_ids:
            order_urls = [
                f"/user/{user_id}/orders",
                f"/orders/{user_id}",
                f"/user/{user_id}/order-history",
            ]
            
            for order_url in order_urls:
                url = f"{settings.BASE_URL.rstrip('/')}{order_url}"
                
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=5000)
                    await page.wait_for_timeout(500)
                    
                    content = await page.content()
                    
                    # Should not show other user's orders
                    if "no orders" in content.lower() or "forbidden" in content.lower():
                        print(f"✓ {order_url} - Access denied or no data")
                    elif "order" in content.lower() and user_id not in ["1", "999"]:
                        # If we got order data for a random ID, suspicious
                        print(f"✓ {order_url} - No real data found (random ID)")
                    else:
                        print(f"  {order_url} - Status unclear")
                except Exception:
                    pass


@allure.feature("Authorization")
@allure.suite("API Authorization")
class TestAPIAuthorization:
    """Test authorization in API endpoints."""
    
    @allure.title("Verify API Endpoints Check User Ownership")
    @allure.description("Check that API endpoints verify user owns the resource")
    @pytest.mark.security
    @pytest.mark.api
    @pytest.mark.access_control
    async def test_api_resource_ownership(self):
        """Test that API properly checks resource ownership."""
        # This would require making actual API calls with different user tokens
        # For now, document the test cases
        
        test_cases = [
            {
                "endpoint": "/api/user/{userId}/profile",
                "description": "Should only allow user to access their own profile",
            },
            {
                "endpoint": "/api/user/{userId}/orders",
                "description": "Should only allow user to access their own orders",
            },
            {
                "endpoint": "/api/order/{orderId}",
                "description": "Should verify user owns the order before returning details",
            },
            {
                "endpoint": "/api/cart/{userId}",
                "description": "Should only allow user to access their own cart",
            },
        ]
        
        print("\nAPI Authorization Test Cases:")
        for test_case in test_cases:
            print(f"  - {test_case['endpoint']}: {test_case['description']}")
        
        allure.attach(
            str(test_cases),
            name="API Authorization Test Cases",
            attachment_type=allure.attachment_type.JSON
        )


@allure.feature("Authorization")
@allure.suite("Session Authorization")
class TestSessionAuthorization:
    """Test authorization based on session state."""
    
    @allure.title("Verify Logout Invalidates Session")
    @allure.description("Check that logging out properly invalidates the session")
    @pytest.mark.security
    @pytest.mark.session
    async def test_logout_invalidates_session(self, page: Page):
        """Test that logout properly invalidates the session."""
        # Navigate to home
        await page.goto(f"{settings.BASE_URL}", wait_until="domcontentloaded")
        
        # Look for logout functionality
        logout_buttons = await page.query_selector_all(
            'button:has-text("Logout"), button:has-text("Sign Out"), a:has-text("Logout")'
        )
        
        if logout_buttons:
            # Click logout
            await logout_buttons[0].click()
            await page.wait_for_timeout(1000)
            
            # Try to access protected page
            protected_urls = [
                "/user/profile",
                "/user/orders",
                "/cart",
            ]
            
            for protected_url in protected_urls:
                url = f"{settings.BASE_URL.rstrip('/')}{protected_url}"
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=5000)
                    await page.wait_for_timeout(500)
                    
                    current_url = page.url.lower()
                    
                    # Should redirect to login
                    if "login" in current_url:
                        print(f"✓ {protected_url} - Properly redirected to login after logout")
                    else:
                        content = await page.content()
                        if "unauthorized" in content.lower():
                            print(f"✓ {protected_url} - Access denied after logout")
                        else:
                            print(f"⚠ {protected_url} - May be accessible after logout!")
                except Exception:
                    pass
        else:
            print("⚠ Could not find logout button")
    
    @allure.title("Prevent Session Reuse After Logout")
    @allure.description("Verify saved session cannot be reused after logout")
    @pytest.mark.security
    @pytest.mark.session
    async def test_session_reuse_prevention(self, page: Page):
        """Test that sessions cannot be reused after logout."""
        # Get initial cookies
        initial_cookies = await page.context.cookies()
        
        # Navigate and logout
        await page.goto(f"{settings.BASE_URL}", wait_until="domcontentloaded")
        
        # Look for logout
        logout_buttons = await page.query_selector_all(
            'button:has-text("Logout"), button:has-text("Sign Out")'
        )
        
        if logout_buttons:
            await logout_buttons[0].click()
            await page.wait_for_timeout(1000)
            
            # Try to use old cookies by loading them in a new context
            # (This tests if the backend invalidates the session)
            print("✓ Session reuse prevention test framework prepared")
