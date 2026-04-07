"""Check what browsers are configured."""
from config import get_settings

settings = get_settings()
print(f"BROWSERS setting: {settings.BROWSERS}")
print(f"Type: {type(settings.BROWSERS)}")
print(f"Length: {len(settings.BROWSERS)}")
for b in settings.BROWSERS:
    print(f"  - {b}")
