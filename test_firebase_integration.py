#!/usr/bin/env python3
# test_firebase_integration.py

import sys
import os

# Add scripts directory to path
sys.path.append('scripts')

def test_firebase_connection():
    """Test Firebase connection"""
    print("🔥 Testing Firebase Integration...")
    
    try:
        # Test Firebase config
        from config.firebase_config import db
        if db:
            print("✅ Firebase connection successful")
            return True
        else:
            print("❌ Firebase connection failed")
            return False
    except Exception as e:
        print(f"❌ Firebase connection error: {e}")
        return False

def test_firebase_manager():
    """Test Firebase manager"""
    print("\n🔧 Testing Firebase Manager...")
    
    try:
        from firebase_manager import FirebaseManager
        firebase = FirebaseManager()
        print("✅ Firebase Manager initialized successfully")
        
        # Test getting tracked products
        products = firebase.get_tracked_products()
        print(f"📋 Found {len(products)} tracked products in Firebase")
        
        # Test getting statistics
        stats = firebase.get_product_statistics()
        print(f"📊 Firebase statistics: {stats}")
        
        return True
    except Exception as e:
        print(f"❌ Firebase Manager error: {e}")
        return False

def test_scraper_integration():
    """Test scraper with Firebase"""
    print("\n🕷️ Testing Scraper with Firebase...")
    
    try:
        from scrape_wee import FIREBASE_ENABLED
        if FIREBASE_ENABLED:
            print("✅ Firebase integration enabled in scraper")
            return True
        else:
            print("⚠️ Firebase integration not enabled in scraper")
            return False
    except Exception as e:
        print(f"❌ Scraper integration error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Firebase Integration Test")
    print("=" * 40)
    
    # Test 1: Firebase Connection
    connection_ok = test_firebase_connection()
    
    # Test 2: Firebase Manager
    manager_ok = test_firebase_manager()
    
    # Test 3: Scraper Integration
    scraper_ok = test_scraper_integration()
    
    # Summary
    print("\n📋 Test Summary:")
    print(f"  🔥 Firebase Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"  🔧 Firebase Manager: {'✅ PASS' if manager_ok else '❌ FAIL'}")
    print(f"  🕷️ Scraper Integration: {'✅ PASS' if scraper_ok else '❌ FAIL'}")
    
    if connection_ok and manager_ok and scraper_ok:
        print("\n🎉 All tests passed! Firebase integration is ready.")
        print("💡 You can now run: python3 scripts/scrape_wee.py")
    else:
        print("\n❌ Some tests failed. Please check your Firebase configuration.")
        print("💡 Make sure you have set up Firebase credentials in your .env file")

if __name__ == "__main__":
    main() 