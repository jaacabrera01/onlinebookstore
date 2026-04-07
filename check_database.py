"""Setup test data by querying what's available and working with it."""
import requests
import json
from config import get_settings

settings = get_settings()


def check_database_status():
    """Check what data exists in the database."""
    print("🔍 Checking BookCart database status...\n")
    
    endpoints = {
        "Books": "/api/Book",
        "Categories": "/api/Book/GetCategoriesList",
        "Users": "/api/User",
    }
    
    for name, endpoint in endpoints.items():
        try:
            response = requests.get(
                f"{settings.BASE_URL.rstrip('/')}{endpoint}",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                count = len(data) if isinstance(data, list) else 1
                print(f"✅ {name:15} - {count} items")
                if isinstance(data, list) and len(data) > 0:
                    print(f"    First item: {json.dumps(data[0], indent=6)[:200]}")
            elif response.status_code == 404:
                print(f"❌ {name:15} - None found (404)")
            else:
                print(f"⚠️  {name:15} - Status {response.status_code}")
        except Exception as e:
            print(f"❌ {name:15} - Error: {str(e)[:50]}")
    
    print("\n" + "="*60)
    print("📋 SUMMARY:")
    print("="*60)
    print("""
The database appears to be empty or just set up. You have these options:

1️⃣  MANUAL SETUP (Easiest):
   - Open the app in your browser
   - Add books through any available admin/management UI
   - This is often the intended way for testing

2️⃣  DATABASE SEED (If available):
   - Check if there's a seed file or migration script
   - Run it against the database
   - Common locations: /sql, /migrations, /scripts

3️⃣  DIRECT DATABASE (If you have access):
   - Connect directly to the database
   - Insert sample book records
   - Check the database schema first

4️⃣  API ADMIN PANEL (If available):
   - Look for admin dashboard at /admin or /management
   - Create books through the UI
   - This is your current bottleneck

🎯 NEXT STEPS:
   1. Check if there's an admin/management interface
   2. Add at least 3-5 books
   3. Rerun your tests
    """)


if __name__ == "__main__":
    check_database_status()
