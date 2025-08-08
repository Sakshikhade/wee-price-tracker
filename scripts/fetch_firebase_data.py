#!/usr/bin/env python3
"""
Firebase Data Fetcher
Fetches and displays data from Firebase Firestore
"""

import sys
import os
from datetime import datetime
from tabulate import tabulate

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from scripts.firebase_manager import FirebaseManager

def fetch_all_products():
    """Fetch all products from Firebase"""
    try:
        firebase = FirebaseManager()
        products = firebase.get_tracked_products()
        
        print("🔥 Firebase Products")
        print("=" * 50)
        
        if products:
            # Prepare data for table
            table_data = []
            for i, product in enumerate(products, 1):
                table_data.append([
                    i,
                    product['name'][:40] + "..." if len(product['name']) > 40 else product['name'],
                    product.get('brand', 'N/A'),
                    product.get('category', 'N/A'),
                    product.get('unit_size', 'N/A')
                ])
            
            headers = ["#", "Product Name", "Brand", "Category", "Unit Size"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
            print(f"\n📊 Total Products: {len(products)}")
        else:
            print("❌ No products found in Firebase")
            
    except Exception as e:
        print(f"❌ Error fetching products: {e}")

def fetch_latest_prices():
    """Fetch latest prices for all products"""
    try:
        firebase = FirebaseManager()
        products = firebase.get_tracked_products()
        
        print("\n💰 Latest Prices")
        print("=" * 50)
        
        if products:
            table_data = []
            for product in products:
                latest_price = firebase.get_latest_price(product['id'])
                if latest_price:
                    table_data.append([
                        product['name'][:35] + "..." if len(product['name']) > 35 else product['name'],
                        latest_price.get('price_str', 'N/A'),
                        latest_price.get('scraped_at', 'N/A').strftime('%Y-%m-%d %H:%M') if latest_price.get('scraped_at') else 'N/A'
                    ])
                else:
                    table_data.append([
                        product['name'][:35] + "..." if len(product['name']) > 35 else product['name'],
                        'No price data',
                        'N/A'
                    ])
            
            headers = ["Product Name", "Latest Price", "Last Updated"]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print("❌ No products found")
            
    except Exception as e:
        print(f"❌ Error fetching prices: {e}")

def fetch_price_history(product_name=None):
    """Fetch price history for a specific product or all products"""
    try:
        firebase = FirebaseManager()
        
        if product_name:
            # Get specific product
            products = [p for p in firebase.get_tracked_products() if product_name.lower() in p['name'].lower()]
            if not products:
                print(f"❌ Product '{product_name}' not found")
                return
        else:
            # Get all products
            products = firebase.get_tracked_products()
        
        print(f"\n📈 Price History")
        print("=" * 50)
        
        for product in products:
            print(f"\n🛍️ {product['name']}")
            print("-" * 30)
            
            # Get price trends
            trends = firebase.get_price_trends(product['id'], days=7)
            if trends:
                table_data = []
                for trend in trends[:5]:  # Show last 5 prices
                    table_data.append([
                        trend.get('scraped_at', 'N/A').strftime('%Y-%m-%d %H:%M') if trend.get('scraped_at') else 'N/A',
                        trend.get('price_str', 'N/A'),
                        f"${trend.get('price', 0):.2f}" if trend.get('price') else 'N/A'
                    ])
                
                headers = ["Date", "Price String", "Price Value"]
                print(tabulate(table_data, headers=headers, tablefmt="simple"))
            else:
                print("  No price history available")
                
    except Exception as e:
        print(f"❌ Error fetching price history: {e}")

def fetch_statistics():
    """Fetch Firebase statistics"""
    try:
        firebase = FirebaseManager()
        stats = firebase.get_product_statistics()
        
        print("\n📊 Firebase Statistics")
        print("=" * 50)
        print(f"📈 Total Products: {stats.get('total_products', 0)}")
        print(f"📊 Total Price Records: {stats.get('total_price_records', 0)}")
        print(f"🚨 Total Alerts: {stats.get('total_alerts', 0)}")
        print(f"💰 Average Price: ${stats.get('avg_price', 0):.2f}")
        print(f"📉 Min Price: ${stats.get('min_price', 0):.2f}")
        print(f"📈 Max Price: ${stats.get('max_price', 0):.2f}")
        
    except Exception as e:
        print(f"❌ Error fetching statistics: {e}")

def main():
    """Main function"""
    print("🔥 Firebase Data Fetcher")
    print("=" * 50)
    
    while True:
        print("\n📋 Choose an option:")
        print("1. Show all products")
        print("2. Show latest prices")
        print("3. Show price history")
        print("4. Show statistics")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            fetch_all_products()
            
        elif choice == '2':
            fetch_latest_prices()
            
        elif choice == '3':
            product_name = input("Enter product name (or press Enter for all): ").strip()
            fetch_price_history(product_name if product_name else None)
            
        elif choice == '4':
            fetch_statistics()
            
        elif choice == '5':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 