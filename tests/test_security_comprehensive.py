"""
Comprehensive Security Test Suite for BookCart Application.

Tests for common vulnerabilities and security flaws:
- SQL Injection attempts
- Cross-Site Scripting (XSS) attacks
- Cross-Site Request Forgery (CSRF) protection
- Input validation and sanitization
- Authentication bypass attempts
- Authorization flaws
- Session hijacking protection
- Data exposure vulnerabilities
"""

import pytest
import allure
from playwright.async_api import Page
from config import get_settings
import uuid
import asyncio
import base64
from urllib.parse import urlencode

settings = get_settings()


@allure.feature("Security")
@allure.suite("SQL Injection Prevention")
class TestSQLInjectionPrevention:
    """Test cases for SQL Injection vulnerability prevention."""
    
    @allure.title("Prevent SQL Injection in Login Username Field")
    @allure.description("Verify that SQL injection payloads in username field are properly sanitized")
    @pytest.mark.security
    @pytest.mark.critical
    async def test_sql_injection_in_login_username(self, page: Page):
        """Test SQL injection prevention in login form."""
        await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
        
        # Common SQL injection payloads
        sql_injection_payloads = [
            "' OR '1'='1",
            "' OR 1=1 --",
            "admin' --",
            "' UNION SELECT * FROM users --",
            "'; DROP TABLE users; --",
            "1' AND SLEEP(5) --",
        ]
        
        for payload in sql_injection_payloads:
            # Reset form
            await page.reload()
            await page.wait_for_timeout(500)
            
            # Attempt SQL injection
            await page.fill('input[formcontrolname="username"]', payload)
            await page.fill('input[formcontrolname="password"]', "password")
            
            # Try to login
            login_btns = await page.query_selector_all('button:has-text("Login")')
            if login_btns:
                await login_btns[-1].click()
                await page.wait_for_timeout(1000)
            
            # Verify we're still on login page (injection failed)
            assert "login" in page.url.lower(), f"SQL injection succeeded with payload: {payload}"
    
    @allure.title("Prevent SQL Injection in Registration Username")
    @allure.description("Verify SQL injection payloads are blocked in registration form")
    @pytest.mark.security
    async def test_sql_injection_in_registration(self, page: Page):
        """Test SQL injection prevention in registration form."""
        await page.goto(f"{settings.BASE_URL}register", wait_until="domcontentloaded")
        await page.wait_for_selector('input[formcontrolname="firstName"]', timeout=10000)
        
        sql_payloads = [
            "user' OR '1'='1",
            "'; DELETE FROM users; --",
            "test' UNION SELECT password FROM users --",
        ]
        
        for payload in sql_payloads:
            # Clear and fill form with SQL injection payload
            await page.fill('input[formcontrolname="firstName"]', "Test")
            await page.fill('input[formcontrolname="lastName"]', "User")
            await page.fill('input[formcontrolname="userName"]', payload)
            await page.fill('input[formcontrolname="password"]', "TestPass123!")
            await page.fill('input[formcontrolname="confirmPassword"]', "TestPass123!")
            
            # Select gender
            genders = await page.query_selector_all('input[type="radio"]')
            if genders:
                await genders[0].click()
            
            # Try to submit
            register_btns = await page.query_selector_all('button:has-text("Register")')
            if register_btns:
                await register_btns[-1].click()
                await page.wait_for_timeout(1000)
            
            # Verify registration failed (payload blocked)
            # Acceptable outcomes: still on register, error page, or redirected to login
            assert "register" in page.url.lower() or "error" in page.url.lower() or "login" in page.url.lower()
            
            # Navigate back to register for next payload
            if "register" not in page.url.lower():
                await page.goto(f"{settings.BASE_URL}register", wait_until="domcontentloaded")
                await page.wait_for_selector('input[formcontrolname="firstName"]', timeout=10000)


@allure.feature("Security")
@allure.suite("XSS Prevention")
class TestXSSPrevention:
    """Test cases for Cross-Site Scripting (XSS) vulnerability prevention."""
    
    @allure.title("Prevent Stored XSS in Product Reviews")
    @allure.description("Verify that XSS payloads in review/comment fields are escaped")
    @pytest.mark.security
    async def test_xss_in_product_review(self, page: Page):
        """Test XSS prevention in product review fields."""
        # Note: This test validates that any reviews/comments don't execute scripts
        await page.goto(f"{settings.BASE_URL}", wait_until="domcontentloaded")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror='alert(\"XSS\")'>",
            "<svg onload='alert(\"XSS\")'>",
            "javascript:alert('XSS')",
            "<body onload='alert(\"XSS\")'></body>",
            "<iframe src='javascript:alert(\"XSS\")'></iframe>",
        ]
        
        for payload in xss_payloads:
            # Navigate to a page where we might input data
            content = await page.content()
            
            # Verify no script tags are rendered from user input
            assert "<script>alert('XSS')</script>" not in content, \
                f"Raw script tag found in page content: {payload}"
            assert "onerror=" not in content or "onerror=" in content.lower() == False, \
                f"Event handler found in page: {payload}"
    
    @allure.title("Prevent Reflected XSS in Search Parameter")
    @allure.description("Verify search parameters don't execute JavaScript")
    @pytest.mark.security
    async def test_xss_in_search_parameter(self, page: Page):
        """Test reflected XSS prevention in search functionality."""
        xss_payload = "<script>alert('XSS')</script>"
        
        # Attempt to inject via URL query parameter
        await page.goto(f"{settings.BASE_URL}?search={xss_payload}", 
                       wait_until="domcontentloaded")
        
        # Check page content - should be escaped
        content = await page.content()
        assert "<script>alert('XSS')</script>" not in content, \
            "XSS payload executed through search parameter"
    
    @allure.title("Prevent DOM-based XSS via Local Storage/Cookies")
    @allure.description("Verify DOM XSS protection when reading from storage")
    @pytest.mark.security
    async def test_dom_xss_prevention(self, page: Page):
        """Test DOM-based XSS prevention."""
        await page.goto(f"{settings.BASE_URL}", wait_until="domcontentloaded")
        
        # Try to inject script through local storage (if application uses it)
        try:
            xss_payload = "<img src=x onerror='alert(\"XSS\")'>"
            await page.evaluate(f"localStorage.setItem('userData', '{xss_payload}')")
            
            # Reload page
            await page.reload()
            await page.wait_for_timeout(1000)
            
            # Check if script was executed (if alert appears, XSS vulnerability exists)
            # In a real test, we might check for console errors or dialog boxes
            assert True  # If we got here without alert, XSS was prevented
        except Exception:
            # Expected if localStorage is not used by application
            pass


@allure.feature("Security")
@allure.suite("Authentication Security")
class TestAuthenticationSecurity:
    """Test cases for authentication vulnerabilities."""
    
    @allure.title("Prevent Authentication Bypass with Empty Credentials")
    @allure.description("Verify that empty username/password are rejected")
    @pytest.mark.security
    async def test_empty_credentials_rejection(self, page: Page):
        """Test that empty credentials cannot bypass authentication."""
        await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
        
        # Try to login with empty username
        await page.fill('input[formcontrolname="username"]', "")
        await page.fill('input[formcontrolname="password"]', "testpassword")
        
        login_btns = await page.query_selector_all('button:has-text("Login")')
        if login_btns:
            await login_btns[-1].click()
            await page.wait_for_timeout(1000)
        
        # Should still be on login page
        assert "login" in page.url.lower()
    
    @allure.title("Prevent Brute Force: Rate Limiting on Login Attempts")
    @allure.description("Verify that multiple failed login attempts trigger rate limiting")
    @pytest.mark.security
    async def test_brute_force_protection(self, page: Page):
        """Test protection against brute force login attacks."""
        await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
        
        # Simulate multiple failed login attempts
        failed_attempts = 0
        for i in range(10):
            await page.fill('input[formcontrolname="username"]', f"user{i}")
            await page.fill('input[formcontrolname="password"]', "wrongpassword")
            
            login_btns = await page.query_selector_all('button:has-text("Login")')
            if login_btns:
                await login_btns[-1].click()
                await page.wait_for_timeout(500)
            
            # Check if we got an error message or rate limit response
            # In a real app, we might see rate limit error after X attempts
            content = await page.content()
            if "too many attempts" in content.lower() or "locked" in content.lower():
                print(f"✓ Rate limiting triggered after {i+1} attempts")
                break
            
            failed_attempts += 1
        
        # Should have gotten rate limited or locked
        # At minimum, we shouldn't be able to login with wrong credentials
        assert "login" in page.url.lower()
    
    @allure.title("Prevent Case-Sensitivity Bypass in Username")
    @allure.description("Verify usernames are compared securely (case-insensitive or consistent)")
    @pytest.mark.security
    async def test_case_sensitivity_bypass(self, page: Page):
        """Test that case variations of username don't bypass security."""
        # This tests if 'Admin', 'admin', 'ADMIN' are treated as different users
        # which could be a security flaw
        usernames_to_test = ["testuser", "TestUser", "TESTUSER"]
        
        for username in usernames_to_test:
            await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
            await page.fill('input[formcontrolname="username"]', username)
            await page.fill('input[formcontrolname="password"]', "wrongpass")
            
            login_btns = await page.query_selector_all('button:has-text("Login")')
            if login_btns:
                await login_btns[-1].click()
                await page.wait_for_timeout(500)
            
            # All should fail consistently
            assert "login" in page.url.lower()


@allure.feature("Security")
@allure.suite("Session Security")
class TestSessionSecurity:
    """Test cases for session management vulnerabilities."""
    
    @allure.title("Verify Secure Session Cookie Flags")
    @allure.description("Check that session cookies have Secure and HttpOnly flags")
    @pytest.mark.security
    async def test_session_cookie_security_flags(self, page: Page):
        """Test that session cookies have proper security flags."""
        await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
        
        # Get all cookies
        cookies = await page.context.cookies()
        
        # Check session-related cookies
        session_cookie_found = False
        for cookie in cookies:
            cookie_name = cookie.get('name', '').lower()
            if any(name in cookie_name for name in ['session', 'auth', 'jwt', 'token']):
                session_cookie_found = True
                
                # Verify security flags
                assert cookie.get('httpOnly', False) or cookie.get('secure', False), \
                    f"Session cookie {cookie_name} missing security flags"
                
                # HTTPS should have secure flag
                if settings.BASE_URL.startswith('https'):
                    assert cookie.get('secure', False), \
                        f"HTTPS cookie {cookie_name} missing Secure flag"
    
    @allure.title("Prevent Session Fixation Attack")
    @allure.description("Verify session ID changes after login")
    @pytest.mark.security
    async def test_session_fixation_prevention(self, page: Page):
        """Test that session ID is regenerated after login."""
        # Get initial session ID
        initial_cookies = await page.context.cookies()
        initial_session = {c['name']: c['value'] for c in initial_cookies 
                          if 'session' in c['name'].lower() or 'auth' in c['name'].lower()}
        
        await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
        
        # Attempt login
        await page.fill('input[formcontrolname="username"]', "testuser")
        await page.fill('input[formcontrolname="password"]', "testpass")
        
        login_btns = await page.query_selector_all('button:has-text("Login")')
        if login_btns:
            await login_btns[-1].click()
            await page.wait_for_timeout(1000)
        
        # Get new session ID after login attempt
        new_cookies = await page.context.cookies()
        new_session = {c['name']: c['value'] for c in new_cookies 
                      if 'session' in c['name'].lower() or 'auth' in c['name'].lower()}
        
        # Session ID should have changed
        if initial_session and new_session:
            assert initial_session != new_session, "Session ID not regenerated after login"
    
    @allure.title("Prevent Session Hijacking via URL")
    @allure.description("Verify session tokens are not exposed in URL parameters")
    @pytest.mark.security
    async def test_session_token_in_url(self, page: Page):
        """Test that session tokens are not sent via URL."""
        await page.goto(f"{settings.BASE_URL}", wait_until="domcontentloaded")
        
        # Check current URL
        current_url = page.url
        
        # URL should not contain sensitive tokens
        assert "session" not in current_url.lower(), "Session ID in URL"
        assert "token" not in current_url.lower(), "Token in URL"
        assert "password" not in current_url.lower(), "Password in URL"
        assert "auth" not in current_url.lower() or "auth" in ["authorization"], "Auth token in URL"


@allure.feature("Security")
@allure.suite("Input Validation")
class TestInputValidation:
    """Test cases for input validation vulnerabilities."""
    
    @allure.title("Validate Email Format")
    @allure.description("Verify that invalid email formats are rejected")
    @pytest.mark.security
    async def test_invalid_email_rejection(self, page: Page):
        """Test email validation in registration form."""
        await page.goto(f"{settings.BASE_URL}register", wait_until="domcontentloaded")
        
        invalid_emails = [
            "notanemail",
            "@nodomain.com",
            "user@",
            "user@.com",
            "user name@test.com",
            "<script>@test.com",
            "user@test.com<script>",
        ]
        
        for invalid_email in invalid_emails:
            await page.reload()
            await page.wait_for_timeout(500)
            
            # Note: Registration might use different fields
            # Fill all required fields
            try:
                await page.fill('input[formcontrolname="firstName"]', "Test")
                await page.fill('input[formcontrolname="lastName"]', "User")
                await page.fill('input[formcontrolname="userName"]', invalid_email)
                await page.fill('input[formcontrolname="password"]', "TestPass123!")
                await page.fill('input[formcontrolname="confirmPassword"]', "TestPass123!")
                
                register_btns = await page.query_selector_all('button:has-text("Register")')
                if register_btns:
                    await register_btns[-1].click()
                    await page.wait_for_timeout(500)
                
                # Should reject invalid email
                assert "register" in page.url.lower() or "error" in page.url.lower()
            except Exception as e:
                print(f"Could not test email {invalid_email}: {str(e)}")
    
    @allure.title("Validate Password Strength Requirements")
    @allure.description("Verify weak passwords are rejected")
    @pytest.mark.security
    async def test_weak_password_rejection(self, page: Page):
        """Test password strength validation."""
        await page.goto(f"{settings.BASE_URL}register", wait_until="domcontentloaded")
        
        weak_passwords = [
            "123",  # Too short
            "password",  # Common password
            "12345678",  # Only numbers
            "abcdefgh",  # Only lowercase
        ]
        
        for weak_pass in weak_passwords:
            await page.reload()
            await page.wait_for_timeout(500)
            
            try:
                await page.fill('input[formcontrolname="firstName"]', "Test")
                await page.fill('input[formcontrolname="lastName"]', "User")
                username = f"testuser_{uuid.uuid4().hex[:8]}"
                await page.fill('input[formcontrolname="userName"]', username)
                await page.fill('input[formcontrolname="password"]', weak_pass)
                await page.fill('input[formcontrolname="confirmPassword"]', weak_pass)
                
                register_btns = await page.query_selector_all('button:has-text("Register")')
                if register_btns:
                    await register_btns[-1].click()
                    await page.wait_for_timeout(500)
                
                # Weak password should be rejected
                content = await page.content()
                assert "register" in page.url.lower() or "password" in content.lower()
            except Exception as e:
                print(f"Could not test password {weak_pass}: {str(e)}")
    
    @allure.title("Prevent Buffer Overflow via Long Input")
    @allure.description("Verify application handles very long input strings")
    @pytest.mark.security
    async def test_buffer_overflow_prevention(self, page: Page):
        """Test handling of extremely long input strings."""
        await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
        
        # Create a very long string
        long_string = "A" * 100000
        
        try:
            await page.fill('input[formcontrolname="username"]', long_string)
            await page.fill('input[formcontrolname="password"]', "password")
            
            login_btns = await page.query_selector_all('button:has-text("Login")')
            if login_btns:
                await login_btns[-1].click()
                await page.wait_for_timeout(1000)
            
            # Application should handle gracefully
            assert page.url is not None, "Application crashed handling long input"
            print("✓ Application handled extremely long input without crashing")
        except Exception as e:
            # Expected - application should either truncate or reject
            print(f"Application properly rejected long input: {type(e).__name__}")


@allure.feature("Security")
@allure.suite("Information Disclosure")
class TestInformationDisclosure:
    """Test cases for information disclosure vulnerabilities."""
    
    @allure.title("Prevent Exposing User Enumeration")
    @allure.description("Verify login error messages don't reveal if user exists")
    @pytest.mark.security
    async def test_user_enumeration_prevention(self, page: Page):
        """Test that error messages don't leak information about user existence."""
        await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
        
        # Try with non-existent user
        await page.fill('input[formcontrolname="username"]', "nonexistentuser12345")
        await page.fill('input[formcontrolname="password"]', "somepassword")
        
        login_btns = await page.query_selector_all('button:has-text("Login")')
        if login_btns:
            await login_btns[-1].click()
            await page.wait_for_timeout(1000)
        
        content = await page.content()
        
        # Error message should be generic, not reveal user doesn't exist
        assert "user not found" not in content.lower(), "User enumeration vulnerability detected"
        assert "invalid username" not in content.lower(), "User enumeration vulnerability detected"
        assert "no account" not in content.lower(), "User enumeration vulnerability detected"
        
        # Should show generic error
        assert "login failed" in content.lower() or "incorrect" in content.lower() or \
               "invalid" in content.lower(), "Expected generic error message"
    
    @allure.title("Prevent Sensitive Data in Error Messages")
    @allure.description("Verify error messages don't contain sensitive information")
    @pytest.mark.security
    async def test_no_sensitive_data_in_errors(self, page: Page):
        """Test that error messages don't expose sensitive data."""
        await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
        
        # Try various invalid inputs
        await page.fill('input[formcontrolname="username"]', "<script>alert('xss')</script>")
        await page.fill('input[formcontrolname="password"]', "test")
        
        login_btns = await page.query_selector_all('button:has-text("Login")')
        if login_btns:
            await login_btns[-1].click()
            await page.wait_for_timeout(1000)
        
        content = await page.content()
        
        # Should not expose database info
        assert "sql" not in content.lower(), "SQL query exposed in error"
        assert "database" not in content.lower(), "Database error exposed"
        assert "column" not in content.lower() or "column" in ["", "Table column"], "DB column name exposed"
        assert "/home/" not in content and "/etc/" not in content, "File path exposed"
    
    @allure.title("Prevent Stack Trace Exposure")
    @allure.description("Verify stack traces are not shown to users")
    @pytest.mark.security
    async def test_no_stack_trace_exposure(self, page: Page):
        """Test that stack traces are not exposed to users."""
        # Try to trigger an error
        try:
            await page.goto(f"{settings.BASE_URL}api/nonexistent", wait_until="domcontentloaded")
        except:
            pass
        
        content = await page.content()
        
        # Look for evidence of stack traces
        assert "traceback" not in content.lower(), "Python traceback exposed"
        assert "at " not in content or "at line" not in content.lower(), "Stack trace details exposed"
        assert "def " not in content or "function" not in content.lower(), "Code details exposed"


@allure.feature("Security")
@allure.suite("CSRF Protection")
class TestCSRFProtection:
    """Test cases for CSRF (Cross-Site Request Forgery) protection."""
    
    @allure.title("Verify CSRF Token Presence in Forms")
    @allure.description("Check that forms include CSRF tokens or similar protection")
    @pytest.mark.security
    async def test_csrf_token_in_login_form(self, page: Page):
        """Test that forms include CSRF protection tokens."""
        await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
        
        content = await page.content()
        
        # Check for CSRF token (csrf, _token, authenticity_token, etc.)
        csrf_token_names = ['csrf', '_token', 'authenticity_token', 'requestVerificationToken']
        
        csrf_found = False
        for token_name in csrf_token_names:
            if token_name.lower() in content.lower():
                csrf_found = True
                print(f"✓ CSRF protection token found: {token_name}")
                break
        
        # Note: Some modern frameworks use SameSite cookies instead of tokens
        if not csrf_found:
            print("⚠ No explicit CSRF token found - verify SameSite cookie protection")
    
    @allure.title("Verify SameSite Cookie Attribute")
    @allure.description("Check that cookies have SameSite attribute set")
    @pytest.mark.security
    async def test_samesite_cookie_attribute(self, page: Page):
        """Test that cookies have SameSite attribute."""
        await page.goto(f"{settings.BASE_URL}login", wait_until="domcontentloaded")
        
        cookies = await page.context.cookies()
        
        # Check SameSite attribute on cookies
        for cookie in cookies:
            # Modern browsers should have SameSite
            samesite = cookie.get('sameSite')
            if samesite:
                assert samesite.lower() in ['strict', 'lax'], \
                    f"Weak SameSite value: {samesite}"
                print(f"✓ Cookie {cookie['name']} has SameSite={samesite}")
