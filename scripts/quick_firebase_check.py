#!/usr/bin/env python3
"""
Quick Firebase Data Check
Quickly check what data is stored in Firebase
"""

import sys
import os
from datetime import datetime

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.firebase_manager import FirebaseManager

def main():
    """Quick check of Firebase data"""
    print("🔥 Quick Firebase Data Check")
    print("=" * 50)
    
    try:
        firebase = FirebaseManager()
        
        # Get statistics
        stats = firebase.get_product_statistics()
        print(f"📊 Total Products: {stats.get('total_products', 0)}")
        print(f"📈 Total Price Records: {stats.get('total_price_records', 0)}")
        print(f"🚨 Total Alerts: {stats.get('total_alerts', 0)}")
        print(f"💰 Average Price: ${stats.get('avg_price', 0):.2f}")
        print(f"📉 Min Price: ${stats.get('min_price', 0):.2f}")
        print(f"📈 Max Price: ${stats.get('max_price', 0):.2f}")
        
        print("\n📋 Products in Firebase:")
        print("-" * 50)
        
        products = firebase.get_tracked_products()
        for i, product in enumerate(products, 1):
            print(f"{i:2d}. {product['name']}")
            
            # Get latest price
            latest_price = firebase.get_latest_price(product['id'])
            if latest_price:
                print(f"    💰 Latest: {latest_price.get('price_str', 'N/A')}")
                print(f"    📅 Updated: {latest_price.get('scraped_at', 'N/A').strftime('%Y-%m-%d %H:%M') if latest_price.get('scraped_at') else 'N/A'}")
            else:
                print(f"    ❌ No price data")
            print()
        
        print(f"\n✅ Firebase is working! Found {len(products)} products with price data.")
        
    except Exception as e:
        print(f"❌ Error checking Firebase: {e}")

if __name__ == "__main__":
    main() 