# scripts/test_price_tracking.py

import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(__file__))

from scrape_wee import (
    TRACKED_PRODUCTS, extract_price_value, load_price_history, 
    save_price_history, send_price_alert, check_price_drops
)

def simulate_price_data():
    """Create sample price data to test the tracking system"""
    
    # Simulate finding our tracked products with prices
    sample_products = [
        {
            "Product Name": "Maggi Masala Instant Noodles 9.8 oz",
            "Price": "$4.99",
            "Unit": "",
            "Brand": "Maggi",
            "Category": "Noodles",
            "Timestamp": datetime.now().isoformat(),
            "Source": "test"
        },
        {
            "Product Name": "Lee Kum Kee Supreme Soy Sauce 500 ml",
            "Price": "$8.99",
            "Unit": "",
            "Brand": "Lee Kum Kee",
            "Category": "Sauces",
            "Timestamp": datetime.now().isoformat(),
            "Source": "test"
        }
    ]
    
    return sample_products

def simulate_price_drop():
    """Simulate a price drop scenario"""
    
    print("🧪 Testing Price Drop Detection System")
    print("=" * 50)
    
    # First, create initial price history
    initial_products = simulate_price_data()
    print("📊 Setting initial prices:")
    for product in initial_products:
        print(f"  {product['Product Name']}: {product['Price']}")
    
    # Save initial prices
    check_price_drops(initial_products)
    
    print("\n⏰ Simulating time passing...")
    print("💰 New prices found with drops:")
    
    # Simulate price drops
    updated_products = [
        {
            "Product Name": "Maggi Masala Instant Noodles 9.8 oz",
            "Price": "$3.99",  # Dropped from $4.99
            "Unit": "",
            "Brand": "Maggi",
            "Category": "Noodles",
            "Timestamp": datetime.now().isoformat(),
            "Source": "test"
        },
        {
            "Product Name": "Lee Kum Kee Supreme Soy Sauce 500 ml",
            "Price": "$7.49",  # Dropped from $8.99
            "Unit": "",
            "Brand": "Lee Kum Kee",
            "Category": "Sauces",
            "Timestamp": datetime.now().isoformat(),
            "Source": "test"
        }
    ]
    
    for product in updated_products:
        print(f"  {product['Product Name']}: {product['Price']}")
    
    print("\n🔍 Checking for price drops...")
    check_price_drops(updated_products)
    
    print("\n✅ Price tracking test completed!")

def test_price_extraction():
    """Test price extraction functionality"""
    
    print("\n🧪 Testing Price Extraction")
    print("=" * 30)
    
    test_prices = [
        "$4.99",
        "$12.50",
        "¥15.99",
        "Price: $8.25",
        "$1,234.56",
        "N/A",
        "",
        "Free"
    ]
    
    for price_str in test_prices:
        extracted = extract_price_value(price_str)
        print(f"'{price_str}' -> {extracted}")

def main():
    """Main test function"""
    print("🛍️ Weee! Price Tracker - Test Suite")
    print("=" * 40)
    
    print(f"📋 Tracking {len(TRACKED_PRODUCTS)} products:")
    for i, product in enumerate(TRACKED_PRODUCTS, 1):
        print(f"  {i}. {product}")
    
    # Test price extraction
    test_price_extraction()
    
    # Test price drop simulation
    simulate_price_drop()
    
    print("\n📁 Check the following files for results:")
    print("  - data/processed/price_history.json")
    print("  - Terminal output above for alerts")

if __name__ == "__main__":
    main()
