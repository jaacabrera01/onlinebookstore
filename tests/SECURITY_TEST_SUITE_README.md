# Comprehensive Security Test Suite for BookCart Application

## Overview

This directory contains an extensive suite of **end-to-end (E2E) and security tests** for the BookCart application. These tests go beyond basic functionality testing to validate **robustness, security, and attack resistance**.

## Test Files Organization

### 1. **test_security_comprehensive.py** - Core Security Tests
Comprehensive security testing covering:
- **SQL Injection Prevention** - Tests for SQL injection in login, registration, search
- **XSS (Cross-Site Scripting) Prevention** - Stored XSS, Reflected XSS, DOM-based XSS
- **Authentication Security** - Empty credentials, brute force protection, case sensitivity
- **Session Security** - Cookie flags, session fixation, session hijacking
- **Input Validation** - Email validation, password strength, buffer overflow prevention
- **Information Disclosure** - User enumeration, sensitive data in errors, stack trace exposure
- **CSRF Protection** - Token presence, SameSite cookies

**Run Tests:**
```bash
pytest tests/test_security_comprehensive.py -v -m security
```

### 2. **test_api_security.py** - REST API Security
Tests for API vulnerabilities:
- **API Authentication** - Unauthenticated access, token validation
- **API Authorization** - Horizontal/vertical privilege escalation, IDOR
- **Rate Limiting** - DDoS protection and rate limiting enforcement
- **Input Validation** - Injection prevention, required fields
- **Response Security** - Security headers, sensitive data leakage
- **API Versioning** - Deprecation handling
- **Endpoint Coverage** - Comprehensive API security audit

**Run Tests:**
```bash
pytest tests/test_api_security.py -v -m api
```

### 3. **test_authorization_security.py** - Access Control & Authorization
Tests for authorization flaws:
- **Access Control** - Admin page protection, role modification prevention
- **Privilege Escalation** - Vertical/horizontal escalation attempts
- **Resource Ownership** - Profile ownership, order access control
- **API Authorization** - Resource ownership verification
- **Session Authorization** - Logout invalidation, session reuse prevention

**Run Tests:**
```bash
pytest tests/test_authorization_security.py -v -m access_control
```

### 4. **test_payment_security.py** - Payment & Checkout Security
Tests for payment processing security:
- **Price Integrity** - Price manipulation prevention, negative prices
- **Quantity Tampering** - Invalid quantity handling
- **Discount Validation** - Discount code injection, stacking prevention
- **Checkout Security** - HTTPS enforcement, logging prevention
- **Order Integrity** - Order total modification, address changes
- **PCI Compliance** - Card data storage, tokenization verification
- **Transaction Validation** - Duplicate prevention, receipt generation

**Run Tests:**
```bash
pytest tests/test_payment_security.py -v -m payment
```

### 5. **test_data_validation.py** - Data Validation & Boundary Testing
Tests for data validation:
- **Boundary Testing** - Maximum/minimum length, numeric boundaries
- **Special Characters** - Character escaping, encoding attacks
- **Type Validation** - Email, number, URL field validation
- **Regex Bypass** - Pattern matching and anchor validation
- **File Upload Security** - File type validation, executable prevention
- **Whitelist Validation** - Country/state selection validation

**Run Tests:**
```bash
pytest tests/test_data_validation.py -v -m data_validation
```

## Test Markers/Categories

Run tests by category using pytest markers:

### By Security Domain
```bash
# SQL Injection tests
pytest -m "sql_injection" -v

# XSS tests
pytest -m "xss" -v

# Authentication tests
pytest -m "auth" -v

# API tests
pytest -m "api" -v

# Payment tests
pytest -m "payment" -v

# Access control tests
pytest -m "access_control" -v
```

### By Severity
```bash
# Critical security issues only
pytest -m "critical" -v

# All security tests
pytest -m "security" -v

# Data validation tests
pytest -m "data_validation" -v
```

## Common Vulnerability Tests Coverage

### OWASP Top 10

| Vulnerability | Test Coverage | File |
|---|---|---|
| Injection (SQL, NoSQL) | ✅ Comprehensive | test_security_comprehensive.py |
| Broken Authentication | ✅ Comprehensive | test_security_comprehensive.py |
| Sensitive Data Exposure | ✅ Comprehensive | test_payment_security.py |
| XML External Entities | ⚠️ Framework dependent | N/A |
| Broken Access Control | ✅ Comprehensive | test_authorization_security.py |
| Security Misconfiguration | ✅ Partial | test_api_security.py |
| Cross-Site Scripting (XSS) | ✅ Comprehensive | test_security_comprehensive.py |
| Insecure Deserialization | ✅ Partial | test_api_security.py |
| Using Components with Known Vulnerabilities | ⚠️ Dependency check needed | External tools |
| Insufficient Logging & Monitoring | ✅ Partial | test_payment_security.py |

### CWE (Common Weakness Enumeration) Coverage

- **CWE-89: SQL Injection** - test_security_comprehensive.py
- **CWE-79: Cross-site Scripting** - test_security_comprehensive.py
- **CWE-352: Cross-Site Request Forgery** - test_security_comprehensive.py
- **CWE-287: Improper Authentication** - test_security_comprehensive.py
- **CWE-639: Authorization Bypass** - test_authorization_security.py
- **CWE-434: Unrestricted File Upload** - test_data_validation.py
- **CWE-434: Path Traversal** - test_authorization_security.py
- **CWE-346: Origin Validation** - test_api_security.py
- **CWE-400: Uncontrolled Resource Consumption** - test_api_security.py
- **CWE-269: Improper Access Control** - test_authorization_security.py

## Running All Security Tests

### Run All Security Tests
```bash
pytest tests/test_security_comprehensive.py \
        tests/test_api_security.py \
        tests/test_authorization_security.py \
        tests/test_payment_security.py \
        tests/test_data_validation.py \
        -v --tb=short
```

### Run with Allure Reporting
```bash
pytest tests/test_security_*.py -v --alluredir=allure-results

# Generate report
allure serve allure-results
```

### Run Specific Test Class
```bash
pytest tests/test_security_comprehensive.py::TestSQLInjectionPrevention -v
```

### Run with Coverage
```bash
pytest tests/test_security_*.py --cov=tests --cov-report=html
```

## Expected Test Results

### Passing Tests (Security Controls Working)
- ✅ SQL injection payloads are rejected
- ✅ XSS attempts are escaped/blocked
- ✅ Authentication is required for protected endpoints
- ✅ Users cannot access other users' data
- ✅ Admin pages require admin role
- ✅ Prices and quantities cannot be manipulated
- ✅ Sessions are invalidated on logout

### Warning Tests (Further Verification Needed)
- ⚠️ Rate limiting not implemented
- ⚠️ CSRF tokens not found (check SameSite cookies)
- ⚠️ API endpoints missing security headers
- ⚠️ Admin section not accessible for full testing

### Failing Tests (Security Vulnerabilities)
- ❌ SQL injection successful
- ❌ XSS payloads executed
- ❌ Unauthenticated access to protected areas
- ❌ Users can access other users' data
- ❌ Price/quantity manipulation possible
- ❌ Session not invalidated on logout

## Test Execution Flow

### Prerequisites
1. **Virtual Environment Activated**
   ```bash
   source .venv/bin/activate
   ```

2. **Dependencies Installed**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variables Set** (if needed)
   ```bash
   export BASE_URL="https://bookcart.azurewebsites.net/"
   ```

### Typical Test Run
```bash
# 1. Run all security tests
pytest tests/test_security_comprehensive.py -v

# 2. Check results
# Expected: Most tests should PASS or show expected SKIPS
# Unexpected: Tests should not FAIL due to vulnerabilities

# 3. Generate report
allure serve allure-results
```

## Test Scenarios & Attack Vectors

### Authentication Testing
- **Empty field submission** - Blank username/password
- **Brute force simulation** - Multiple failed attempts
- **Credential stuffing** - Common passwords
- **Case sensitivity bypass** - Username case variations
- **SQL injection** - ' OR '1'='1 variants

### Authorization Testing
- **Direct object reference** - Access other users' orders
- **Privilege escalation** - User becoming admin
- **Role bypass** - Accessing admin features
- **URL manipulation** - Direct URL parameter changes
- **Hidden field manipulation** - Changing role via form fields

### Data Injection Testing
- **SQL Injection** - Database manipulation
- **Cross-Site Scripting** - JavaScript injection
- **Command Injection** - OS command execution
- **LDAP Injection** - Directory service manipulation
- **XML Entity Injection** - File inclusion

### API Security Testing
- **Unauthenticated access** - Accessing without token
- **Malformed tokens** - Invalid JWT/Bearer tokens
- **Token tampering** - Modifying token content
- **Missing validation** - Required field omission
- **Response data leakage** - Sensitive info in responses

### Payment Security Testing
- **Price manipulation** - Changing item prices
- **Quantity tampering** - Invalid quantities
- **Discount stacking** - Multiple discount codes
- **Order total modification** - Changing final amount
- **Address hijacking** - Changing shipping address

## Troubleshooting Tests

### Tests Timeout
**Issue:** Tests taking too long or timing out
```bash
# Increase timeout
pytest tests/test_security_comprehensive.py --timeout=60
```

### WebDriver Issues
**Issue:** Playwright/browser issues
```bash
# Reinstall browsers
playwright install

# Run single test with verbose output
pytest tests/test_security_comprehensive.py::TestSQLInjectionPrevention::test_sql_injection_in_login_username -vvs
```

### API Tests Can't Connect
**Issue:** API endpoint not responding
```bash
# Verify API is reachable
curl https://bookcart.azurewebsites.net/api/books

# Check config
python -c "from config import get_settings; print(get_settings().API_BASE_URL)"
```

## Best Practices for Security Testing

1. **Run Regularly**
   - Run before each release
   - Include in CI/CD pipeline
   - Run against staging environment

2. **Document Findings**
   - Create issue for each vulnerability found
   - Include test name and payload
   - Add reproduction steps

3. **Fix Vulnerabilities**
   - Address critical issues immediately
   - Implement fixes
   - Re-run tests to verify

4. **Update Tests**
   - Add test for new vulnerabilities found
   - Remove obsolete tests
   - Keep test data files updated

5. **Review Attack Vectors**
   - Monitor security advisories
   - Update payloads based on new techniques
   - Test emerging attack vectors

## Security Testing Checklist

Before release, ensure:

- [ ] All security tests executed
- [ ] No CRITICAL vulnerabilities found
- [ ] SQL injection prevention verified
- [ ] XSS protection confirmed
- [ ] Authentication required for protected areas
- [ ] Authorization checks working
- [ ] HTTPS enforced on sensitive operations
- [ ] No sensitive data in logs/errors
- [ ] Rate limiting in place
- [ ] CSRF tokens/SameSite cookies present
- [ ] File uploads properly validated
- [ ] Session management working correctly

## Integration with CI/CD

### GitHub Actions Example
```yaml
- name: Run Security Tests
  run: |
    pytest tests/test_security_*.py -v \
            --junitxml=results.xml \
            --alluredir=allure-results
    
- name: Publish Test Results
  uses: EnricoMi/publish-unit-test-result-action@v2
  if: always()
  with:
    files: results.xml
```

### Jenkins Example
```groovy
stage('Security Testing') {
    steps {
        sh 'pytest tests/test_security_*.py -v --junitxml=results.xml'
        junit 'results.xml'
    }
}
```

## References

- **OWASP Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/
- **CWE List**: https://cwe.mitre.org/
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Playwright Docs**: https://playwright.dev/python/
- **Pytest Docs**: https://docs.pytest.org/

## Contributing

To add new security tests:

1. Create test in appropriate file based on vulnerability type
2. Use clear test name: `test_<vulnerability>_<scenario>`
3. Add `@pytest.mark.security` and category marker
4. Include documentation with `@allure.description`
5. Test with both positive and negative cases
6. Update this README with new test coverage

## Support

For questions about specific security tests:
- Review test docstrings and comments
- Check Allure reports for detailed test results
- Run test with `-vvs` flag for verbose output
- Refer to test file comments for vulnerability details

---

**Last Updated:** April 2026
**Test Suite Version:** 1.0
**Compatible with:** Pytest 7.0+, Playwright 1.40+
