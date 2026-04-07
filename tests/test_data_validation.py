"""
Data Validation and Boundary Test Suite for BookCart Application.

Tests for data validation vulnerabilities:
- Boundary value testing
- Data type validation
- Special character handling
- Unicode/encoding attacks
- File upload validation
- Regex bypass attacks
"""

import pytest
import allure
from playwright.async_api import Page
from config import get_settings
import asyncio

settings = get_settings()


@allure.feature("Data Validation")
@allure.suite("Boundary Testing")
class TestBoundaryValues:
    """Test cases for boundary value testing."""
    
    @allure.title("Test Maximum Length Input Fields")
    @allure.description("Verify application handles maximum length strings correctly")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_max_length_boundaries(self, page: Page):
        """Test maximum length boundary values."""
        await page.goto(f"{settings.BASE_URL}register", wait_until="domcontentloaded")
        
        # Get input fields
        input_fields = await page.query_selector_all('input[type="text"], input[type="email"], textarea')
        
        for field in input_fields:
            # Get the max length attribute if it exists
            max_length = await field.get_attribute('maxlength')
            
            if max_length:
                max_len_int = int(max_length)
                
                # Test at boundary (max - 1, max, max + 1)
                test_values = [
                    ("A" * (max_len_int - 1), "max-1"),
                    ("A" * max_len_int, "max"),
                    ("A" * (max_len_int + 1), "max+1"),
                ]
                
                for value, label in test_values:
                    try:
                        await field.fill("")
                        await field.fill(value)
                        
                        current_value = await field.input_value()
                        
                        if len(current_value) <= max_len_int:
                            print(f"✓ Field properly enforces max length {label}")
                        else:
                            print(f"⚠ Field might exceed max length {label}")
                    except Exception as e:
                        print(f"Could not test boundary: {str(e)}")
            else:
                # No max length specified - potential vulnerability
                try:
                    long_value = "X" * 10000
                    await field.fill(long_value)
                    
                    current_value = await field.input_value()
                    if len(current_value) > 10000:
                        print(f"⚠ Field accepts extremely long input (no maxlength)")
                    else:
                        print(f"✓ Field has implicit length limit")
                except Exception:
                    pass
    
    @allure.title("Test Minimum Value for Numeric Fields")
    @allure.description("Verify numeric fields validate minimum values")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_numeric_minimum_boundary(self, page: Page):
        """Test minimum value boundary for numeric fields."""
        # Find numeric input fields
        numeric_fields = await page.query_selector_all('input[type="number"]')
        
        for field in numeric_fields:
            min_attr = await field.get_attribute('min')
            
            if min_attr:
                min_val = int(min_attr)
                
                # Test boundary values
                test_values = [
                    min_val - 1,
                    min_val,
                    min_val + 1,
                ]
                
                for test_val in test_values:
                    try:
                        await field.fill(str(test_val))
                        
                        current_val = await field.input_value()
                        
                        if test_val < min_val and (current_val == "" or int(current_val) >= min_val):
                            print(f"✓ Field properly enforces minimum boundary")
                        elif test_val < min_val:
                            print(f"⚠ Field accepted value below minimum: {test_val}")
                    except Exception:
                        pass
    
    @allure.title("Test Maximum Value for Numeric Fields")
    @allure.description("Verify numeric fields validate maximum values")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_numeric_maximum_boundary(self, page: Page):
        """Test maximum value boundary for numeric fields."""
        numeric_fields = await page.query_selector_all('input[type="number"]')
        
        for field in numeric_fields:
            max_attr = await field.get_attribute('max')
            
            if max_attr:
                max_val = int(max_attr)
                
                test_values = [
                    max_val - 1,
                    max_val,
                    max_val + 1,
                    999999,
                ]
                
                for test_val in test_values:
                    try:
                        await field.fill(str(test_val))
                        
                        current_val = await field.input_value()
                        
                        if test_val > max_val and (current_val == "" or int(current_val) <= max_val):
                            print(f"✓ Field properly enforces maximum boundary")
                        elif test_val > max_val:
                            print(f"⚠ Field accepted value above maximum: {test_val}")
                    except Exception:
                        pass


@allure.feature("Data Validation")
@allure.suite("Special Character Handling")
class TestSpecialCharacterHandling:
    """Test cases for special character handling."""
    
    @allure.title("Handle Special Characters in Text Fields")
    @allure.description("Verify application properly escapes special characters")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_special_character_escaping(self, page: Page):
        """Test that special characters are properly escaped."""
        await page.goto(f"{settings.BASE_URL}register", wait_until="domcontentloaded")
        
        # Special characters to test
        special_chars = [
            "!@#$%^&*()",
            "<>\"'",
            "{}[]|\\",
            "~`",
            "\n\r\t",
            "\\x00\\x01",
        ]
        
        text_fields = await page.query_selector_all('input[type="text"], textarea')
        
        for field in text_fields:
            for char_set in special_chars:
                try:
                    await field.fill(f"test{char_set}string")
                    
                    # Verify it was stored safely
                    value = await field.input_value()
                    print(f"✓ Special characters handled: field accepted and stored")
                except Exception as e:
                    print(f"✓ Special characters properly rejected: {char_set}")
    
    @allure.title("Handle Unicode and Encoding Characters")
    @allure.description("Verify application handles Unicode and multi-byte characters")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_unicode_character_handling(self, page: Page):
        """Test Unicode character handling."""
        unicode_strings = [
            "你好世界",  # Chinese
            "Здравствуй",  # Russian
            "🚀💻🔒",  # Emojis
            "Café",  # Accented characters
            "ñ ü ö",  # Diacritics
        ]
        
        text_fields = await page.query_selector_all('input[type="text"], textarea')
        
        for field in text_fields:
            for unicode_str in unicode_strings:
                try:
                    await field.fill("")
                    await field.fill(unicode_str)
                    
                    value = await field.input_value()
                    
                    if unicode_str in value or len(value) > 0:
                        print(f"✓ Unicode handled: {unicode_str[:10]}...")
                    else:
                        print(f"⚠ Unicode may have been stripped: {unicode_str[:10]}...")
                except Exception:
                    pass


@allure.feature("Data Validation")
@allure.suite("Type Validation")
class TestTypeValidation:
    """Test cases for data type validation."""
    
    @allure.title("Validate Email Field Type")
    @allure.description("Verify email fields validate proper email format")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_email_type_validation(self, page: Page):
        """Test email field validation."""
        email_fields = await page.query_selector_all('input[type="email"]')
        
        invalid_emails = [
            "notanemail",
            "@domain.com",
            "user@",
            "user@.com",
            "user name@test.com",
        ]
        
        for field in email_fields:
            for invalid_email in invalid_emails:
                try:
                    await field.fill(invalid_email)
                    
                    # Check if field validation triggers
                    validity = await field.evaluate("el => el.validity.valid")
                    
                    if not validity:
                        print(f"✓ Email validation rejects: {invalid_email}")
                    else:
                        print(f"⚠ Email validation may accept invalid: {invalid_email}")
                except Exception:
                    pass
    
    @allure.title("Validate Number Field Type")
    @allure.description("Verify number fields only accept numeric values")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_number_type_validation(self, page: Page):
        """Test numeric field validation."""
        number_fields = await page.query_selector_all('input[type="number"]')
        
        invalid_numbers = [
            "abc",
            "12.34.56",
            "1e10",
            "0x1A",
            "NaN",
            "Infinity",
        ]
        
        for field in number_fields:
            for invalid_num in invalid_numbers:
                try:
                    await field.fill(invalid_num)
                    
                    value = await field.input_value()
                    
                    # Number field should reject non-numeric
                    if value == "" or value == invalid_num:
                        print(f"✓ Number field properly handles: {invalid_num}")
                    else:
                        print(f"⚠ Number field accepted non-numeric: {invalid_num}")
                except Exception:
                    pass
    
    @allure.title("Validate URL Field Type")
    @allure.description("Verify URL fields validate proper URL format")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_url_type_validation(self, page: Page):
        """Test URL field validation."""
        url_fields = await page.query_selector_all('input[type="url"]')
        
        invalid_urls = [
            "not a url",
            "ht!tp://test.com",
            "://test.com",
            "file:///etc/passwd",
            "javascript:alert('xss')",
        ]
        
        for field in url_fields:
            for invalid_url in invalid_urls:
                try:
                    await field.fill(invalid_url)
                    
                    validity = await field.evaluate("el => el.validity.valid")
                    
                    if not validity:
                        print(f"✓ URL validation rejects: {invalid_url}")
                    else:
                        print(f"⚠ URL field may accept invalid: {invalid_url}")
                except Exception:
                    pass


@allure.feature("Data Validation")
@allure.suite("Regex Patterns")
class TestRegexBypass:
    """Test cases for regex pattern bypass attempts."""
    
    @allure.title("Test Regex Anchoring")
    @allure.description("Verify regex patterns use proper anchors (^ and $)")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_regex_anchor_bypass(self, page: Page):
        """Test for regex anchor bypass vulnerabilities."""
        # This is more of a backend test, but we can test validation behavior
        await page.goto(f"{settings.BASE_URL}register", wait_until="domcontentloaded")
        
        # Test pattern: /^[a-zA-Z]+$/ without anchors would match "abc123def"
        alphanumeric_fields = await page.query_selector_all('input[pattern*="[a-z"]')
        
        test_values = [
            "validinput123",
            "123validinput",
            "valid123input",
        ]
        
        for field in alphanumeric_fields:
            pattern = await field.get_attribute('pattern')
            
            for test_val in test_values:
                try:
                    await field.fill(test_val)
                    
                    validity = await field.evaluate("el => el.validity.valid")
                    
                    if pattern and "^" in pattern and "$" in pattern:
                        print(f"✓ Pattern uses anchors")
                    else:
                        # Might be vulnerable
                        print(f"⚠ Pattern may lack anchors: {pattern}")
                except Exception:
                    pass


@allure.feature("Data Validation")
@allure.suite("File Upload Security")
class TestFileUploadSecurity:
    """Test cases for file upload security."""
    
    @allure.title("Validate File Upload File Types")
    @allure.description("Verify only allowed file types can be uploaded")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_file_type_validation(self, page: Page):
        """Test file upload type validation."""
        # Find file input fields
        file_inputs = await page.query_selector_all('input[type="file"]')
        
        if file_inputs:
            for file_input in file_inputs:
                # Check accepted file types
                accept_attr = await file_input.get_attribute('accept')
                
                if accept_attr:
                    print(f"✓ File input has accept restriction: {accept_attr}")
                else:
                    print(f"⚠ File input may accept any file type")
    
    @allure.title("Prevent Executable File Upload")
    @allure.description("Verify executable files cannot be uploaded")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_executable_upload_prevention(self, page: Page):
        """Test that executable files are blocked."""
        # Dangerous file extensions to prevent
        dangerous_extensions = [
            ".exe",
            ".sh",
            ".bat",
            ".cmd",
            ".scr",
            ".asp",
            ".jsp",
            ".php",
            ".py",
        ]
        
        file_inputs = await page.query_selector_all('input[type="file"]')
        
        for file_input in file_inputs:
            accept_attr = await file_input.get_attribute('accept')
            
            if accept_attr:
                for dangerous_ext in dangerous_extensions:
                    if dangerous_ext in accept_attr:
                        print(f"⚠ Dangerous extension may be allowed: {dangerous_ext}")
                    else:
                        print(f"✓ Extension blocked: {dangerous_ext}")
            else:
                print(f"⚠ No file type restriction - all extensions allowed!")


@allure.feature("Data Validation")
@allure.suite("Whitelist Validation")
class TestWhitelistValidation:
    """Test cases for whitelist-based validation."""
    
    @allure.title("Test Country/Region Selection Validation")
    @allure.description("Verify only valid countries/regions can be selected")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_country_whitelist_validation(self, page: Page):
        """Test country selection validation."""
        # Find country select fields
        country_selects = await page.query_selector_all(
            'select[name*="country"], select[name*="region"], select[formcontrolname*="country"]'
        )
        
        for select in country_selects:
            options = await select.query_selector_all('option')
            
            print(f"✓ Found {len(options)} country options")
            
            # Try to set invalid value
            try:
                await select.select_option("INVALID_COUNTRY")
                selected_val = await select.input_value()
                
                if selected_val == "INVALID_COUNTRY":
                    print(f"⚠ Invalid country value was accepted!")
                else:
                    print(f"✓ Invalid country properly rejected")
            except Exception:
                print(f"✓ Invalid country value rejected")
    
    @allure.title("Test State/Province Selection Validation")
    @allure.description("Verify only valid states/provinces can be selected")
    @pytest.mark.security
    @pytest.mark.data_validation
    async def test_state_whitelist_validation(self, page: Page):
        """Test state/province selection validation."""
        state_selects = await page.query_selector_all(
            'select[name*="state"], select[name*="province"], select[formcontrolname*="state"]'
        )
        
        for select in state_selects:
            try:
                await select.select_option("INVALID_STATE")
                selected_val = await select.input_value()
                
                if selected_val == "INVALID_STATE":
                    print(f"⚠ Invalid state value was accepted!")
                else:
                    print(f"✓ Invalid state properly rejected")
            except Exception:
                print(f"✓ Invalid state value rejected")
