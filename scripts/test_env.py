#!/usr/bin/env python3
# scripts/test_env_fixed.py - Fixed environment test script

import os
import sys
import json
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Now import dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ python-dotenv loaded successfully")
except ImportError:
    print("❌ python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)

def test_env_loading():
    """Test environment variable loading"""
    
    print("🧪 Testing Environment Variable Loading")
    print("=" * 50)
    
    print("✅ .env file loaded")
    
    # Test email configuration
    print("\n📧 Email Configuration:")
    print(f"  SMTP Server: {os.getenv('EMAIL_SMTP_SERVER', 'Not set')}")
    print(f"  SMTP Port: {os.getenv('EMAIL_SMTP_PORT', 'Not set')}")
    print(f"  Sender Email: {os.getenv('EMAIL_SENDER_ADDRESS', 'Not set')}")
    print(f"  Sender Name: {os.getenv('EMAIL_SENDER_NAME', 'Not set')}")
    
    # Check if password is set (don't show the actual password)
    password = os.getenv('EMAIL_SENDER_PASSWORD', 'Not set')
    if password != 'Not set' and password != 'your_app_password':
        print(f"  Sender Password: {'*' * len(password)} (configured)")
    else:
        print(f"  Sender Password: {password}")
    
    # Test alert settings
    print("\n�� Alert Settings:")
    print(f"  Alerts Enabled: {os.getenv('EMAIL_ENABLE_ALERTS', 'Not set')}")
    print(f"  Max Alerts/Day: {os.getenv('EMAIL_MAX_ALERTS_PER_DAY', 'Not set')}")
    print(f"  Cooldown Hours: {os.getenv('EMAIL_ALERT_COOLDOWN_HOURS', 'Not set')}")
    print(f"  Subject Prefix: {os.getenv('EMAIL_SUBJECT_PREFIX', 'Not set')}")
    
    # Test product tracking
    print("\n🛍️ Product Tracking:")
    tracked_products_str = os.getenv('TRACKED_PRODUCTS', 'Not set')
    if tracked_products_str != 'Not set':
        try:
            products = json.loads(tracked_products_str)
            print(f"  Tracked Products: {len(products)}")
            for i, product in enumerate(products, 1):
                print(f"    {i}. {product}")
        except json.JSONDecodeError:
            print(f"  ❌ Invalid JSON format: {tracked_products_str}")
    else:
        print(f"  Tracked Products: {tracked_products_str}")
    
    # Test web scraping
    print("\n🌐 Web Scraping:")
    print(f"  Base URL: {os.getenv('BASE_URL', 'Not set')}")
    print(f"  Request Timeout: {os.getenv('REQUEST_TIMEOUT', 'Not set')}")
    print(f"  Max Retries: {os.getenv('MAX_RETRIES', 'Not set')}")
    
    print("\n✅ Environment variable test complete!")

def test_email_config_integration():
    """Test email configuration integration"""
    
    print("\n🔗 Testing Email Configuration Integration")
    print("=" * 50)
    
    try:
        # Import with proper path setup
        from config.email_config import EMAIL_SERVER_CONFIG, GLOBAL_ALERT_SETTINGS
        print("✅ Email config imported successfully")
        
        print(f"📧 SMTP Server: {EMAIL_SERVER_CONFIG['smtp_server']}")
        print(f"📧 SMTP Port: {EMAIL_SERVER_CONFIG['smtp_port']}")
        print(f"📧 Sender Email: {EMAIL_SERVER_CONFIG['sender_email']}")
        print(f"📧 Sender Name: {EMAIL_SERVER_CONFIG['sender_name']}")
        
        # Check password (don't show actual value)
        password = EMAIL_SERVER_CONFIG['sender_password']
        if password != 'your_app_password':
            print(f"📧 Sender Password: {'*' * len(password)} (configured)")
        else:
            print(f"�� Sender Password: {password}")
        
        print(f"�� Alerts Enabled: {GLOBAL_ALERT_SETTINGS['enable_alerts']}")
        print(f"�� Max Alerts/Day: {GLOBAL_ALERT_SETTINGS['max_alerts_per_day']}")
        print(f"�� Cooldown Hours: {GLOBAL_ALERT_SETTINGS['alert_cooldown_hours']}")
        
    except ImportError as e:
        print(f"❌ Failed to import email config: {e}")
        print("💡 Make sure config/email_config.py exists")
    except Exception as e:
        print(f"❌ Error testing email config: {e}")

def test_scraper_integration():
    """Test scraper integration"""
    
    print("\n🕷️ Testing Scraper Integration")
    print("=" * 50)
    
    try:
        # Import with proper path setup
        from scripts.scrape_wee import TRACKED_PRODUCTS, BASE_URL
        print("✅ Scraper config imported successfully")
        
        print(f"��️ Tracked Products: {len(TRACKED_PRODUCTS)}")
        for i, product in enumerate(TRACKED_PRODUCTS, 1):
            print(f"  {i}. {product}")
        
        print(f"🌐 Base URL: {BASE_URL}")
        
    except ImportError as e:
        print(f"❌ Failed to import scraper config: {e}")
        print("💡 Make sure scripts/scrape_wee.py exists")
    except Exception as e:
        print(f"❌ Error testing scraper config: {e}")

def main():
    """Main test function"""
    
    print("🔐 Environment Variables Test Suite")
    print("=" * 40)
    
    # Test basic environment loading
    test_env_loading()
    
    # Test email configuration integration
    test_email_config_integration()
    
    # Test scraper integration
    test_scraper_integration()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()