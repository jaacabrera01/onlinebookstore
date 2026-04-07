"""API helper for backend testing and validation."""
import requests
from typing import Dict, Any, Optional
from config import get_settings


settings = get_settings()


class APIClient:
    """Client for making API requests."""
    
    def __init__(self, base_url: str = settings.BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "BookCart-Automation/1.0"
        })
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """Make GET request."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return self.session.get(url, timeout=30, **kwargs)
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Make POST request."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return self.session.post(url, json=data, timeout=30, **kwargs)
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Make PUT request."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return self.session.put(url, json=data, timeout=30, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make DELETE request."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        return self.session.delete(url, timeout=30, **kwargs)
    
    def close(self):
        """Close session."""
        self.session.close()


def assert_response(
    response: requests.Response,
    expected_status: int,
    message: str = ""
):
    """Assert response status code."""
    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, got {response.status_code}. "
        f"Response: {response.text}. {message}"
    )


def assert_response_contains(
    response: requests.Response,
    key: str,
    expected_value: Any = None,
    message: str = ""
):
    """Assert response JSON contains expected key/value."""
    try:
        data = response.json()
    except ValueError:
        raise AssertionError(f"Response is not valid JSON: {response.text}")
    
    assert key in data, f"Key '{key}' not found in response. {message}"
    
    if expected_value is not None:
        assert data[key] == expected_value, (
            f"Expected {key}='{expected_value}', got '{data[key]}'. {message}"
        )
