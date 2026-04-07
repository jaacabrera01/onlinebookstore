"""Discover API endpoints from Swagger."""
import requests
import json
from config import get_settings

settings = get_settings()

def discover_swagger_api():
    """Fetch and display Swagger API documentation."""
    swagger_urls = [
        f"{settings.BASE_URL.rstrip('/')}/swagger/v1/swagger.json",
        f"{settings.BASE_URL.rstrip('/')}/api/swagger.json",
        f"{settings.BASE_URL.rstrip('/')}/swagger.json",
        f"{settings.BASE_URL.rstrip('/')}/api-docs",
    ]
    
    print("🔍 Looking for Swagger documentation...\n")
    
    for url in swagger_urls:
        try:
            print(f"Trying: {url}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Found at: {url}\n")
                data = response.json()
                
                # Display available endpoints
                if "paths" in data:
                    print("📍 Available API Endpoints:")
                    print("=" * 60)
                    for path, methods in sorted(data["paths"].items()):
                        for method in methods.keys():
                            if method.upper() in ["GET", "POST", "PUT", "DELETE"]:
                                print(f"  {method.upper():6} {path}")
                    
                    print("\n📄 Base path:", data.get("basePath", "/"))
                    print("📦 Server URL(s):", data.get("servers", "N/A"))
                    
                    # Show schemas/models
                    if "components" in data and "schemas" in data["components"]:
                        print("\n📋 Data Models Available:")
                        print("=" * 60)
                        for schema_name in list(data["components"]["schemas"].keys())[:10]:
                            print(f"  - {schema_name}")
                
                return True
        except Exception as e:
            print(f"❌ Failed: {str(e)}")
    
    print("\n⚠️  No Swagger documentation found at expected URLs")
    print("   Try accessing the site directly and looking for:")
    print("   - '/swagger' path")
    print("   - '/api-docs' path")
    print("   - 'Swagger UI' link in the navigation")

if __name__ == "__main__":
    discover_swagger_api()
