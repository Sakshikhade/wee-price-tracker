#!/usr/bin/env python3
# scripts/firebase_analytics.py

import sys
import os
from datetime import datetime, timedelta
import pandas as pd

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from firebase_manager import FirebaseManager

class FirebaseAnalytics:
    def __init__(self):
        self.firebase = FirebaseManager()
    
    def get_price_trends(self, product_name=None, days=30):
        """Get price trends for products"""
        try:
            if product_name:
                # Get specific product trends
                products = self.firebase.get_tracked_products()
                product_id = None
                for product in products:
                    if product['name'] == product_name:
                        product_id = product['id']
                        break
                
                if product_id:
                    trends = self.firebase.get_price_trends(product_id, days)
                    return trends
                else:
                    print(f"❌ Product '{product_name}' not found")
                    return []
            else:
                # Get all product trends
                products = self.firebase.get_tracked_products()
                all_trends = {}
                
                for product in products:
                    trends = self.firebase.get_price_trends(product['id'], days)
                    if trends:
                        all_trends[product['name']] = trends
                
                return all_trends
                
        except Exception as e:
            print(f"❌ Error getting price trends: {e}")
            return {}
    
    def get_biggest_savings(self, days=7):
        """Get products with biggest savings"""
        try:
            savings = self.firebase.get_biggest_savings(days)
            return savings
        except Exception as e:
            print(f"❌ Error getting biggest savings: {e}")
            return []
    
    def get_product_statistics(self):
        """Get overall product statistics"""
        try:
            stats = self.firebase.get_product_statistics()
            return stats
        except Exception as e:
            print(f"❌ Error getting product statistics: {e}")
            return {}
    
    def generate_report(self):
        """Generate comprehensive analytics report"""
        print("📊 Firebase Analytics Report")
        print("=" * 50)
        
        # Get statistics
        stats = self.get_product_statistics()
        if stats:
            print(f"📈 Total Products: {stats.get('total_products', 0)}")
            print(f"📊 Total Price Records: {stats.get('total_price_records', 0)}")
            print(f"🚨 Total Alerts: {stats.get('total_alerts', 0)}")
            print(f"💰 Average Price: ${stats.get('avg_price', 0):.2f}")
            print(f"📉 Min Price: ${stats.get('min_price', 0):.2f}")
            print(f"📈 Max Price: ${stats.get('max_price', 0):.2f}")
        
        print("\n🏆 Biggest Savings (Last 7 Days):")
        savings = self.get_biggest_savings(7)
        if savings:
            for i, saving in enumerate(savings[:5], 1):
                print(f"  {i}. {saving['product_name']}")
                print(f"     ${saving['old_price']} → ${saving['new_price']}")
                print(f"     Save: ${saving['savings_amount']:.2f} ({saving['savings_percentage']:.1f}%)")
                print()
        else:
            print("  No recent savings found")
        
        print("\n📋 Tracked Products:")
        products = self.firebase.get_tracked_products()
        if products:
            for i, product in enumerate(products[:10], 1):
                print(f"  {i}. {product['name']}")
            if len(products) > 10:
                print(f"  ... and {len(products) - 10} more products")
        else:
            print("  No tracked products found")
    
    def export_to_csv(self, filename="firebase_analytics.csv"):
        """Export analytics data to CSV"""
        try:
            # Get all products and their latest prices
            products = self.firebase.get_tracked_products()
            data = []
            
            for product in products:
                latest_price = self.firebase.get_latest_price(product['id'])
                if latest_price:
                    data.append({
                        'Product Name': product['name'],
                        'Brand': product.get('brand', ''),
                        'Category': product.get('category', ''),
                        'Unit Size': product.get('unit_size', ''),
                        'Latest Price': latest_price.get('price', 0),
                        'Price String': latest_price.get('price_str', ''),
                        'Last Updated': latest_price.get('scraped_at', ''),
                        'Priority': product.get('priority', 1)
                    })
            
            if data:
                df = pd.DataFrame(data)
                df.to_csv(filename, index=False)
                print(f"✅ Exported {len(data)} products to {filename}")
                return True
            else:
                print("❌ No data to export")
                return False
                
        except Exception as e:
            print(f"❌ Error exporting to CSV: {e}")
            return False

def main():
    """Main analytics function"""
    import sys
    
    analytics = FirebaseAnalytics()
    
    # Check for command line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--report-only':
        # Generate report only for automated scripts
        analytics.generate_report()
        return
    
    print("🔥 Firebase Analytics Dashboard")
    print("=" * 50)
    
    while True:
        print("\n📊 Choose an option:")
        print("1. Generate full report")
        print("2. Get price trends for a product")
        print("3. Get biggest savings")
        print("4. Export data to CSV")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            analytics.generate_report()
            
        elif choice == '2':
            product_name = input("Enter product name: ").strip()
            if product_name:
                trends = analytics.get_price_trends(product_name, 30)
                if trends:
                    print(f"\n📈 Price trends for '{product_name}':")
                    for trend in trends[:10]:
                        print(f"  {trend['scraped_at']}: {trend['price_str']}")
                else:
                    print("❌ No trends found for this product")
            
        elif choice == '3':
            days = input("Enter number of days (default 7): ").strip()
            days = int(days) if days.isdigit() else 7
            
            savings = analytics.get_biggest_savings(days)
            if savings:
                print(f"\n🏆 Biggest savings (last {days} days):")
                for i, saving in enumerate(savings[:10], 1):
                    print(f"  {i}. {saving['product_name']}")
                    print(f"     ${saving['old_price']} → ${saving['new_price']}")
                    print(f"     Save: ${saving['savings_amount']:.2f} ({saving['savings_percentage']:.1f}%)")
            else:
                print("❌ No savings found")
                
        elif choice == '4':
            filename = input("Enter filename (default: firebase_analytics.csv): ").strip()
            filename = filename if filename else "firebase_analytics.csv"
            analytics.export_to_csv(filename)
            
        elif choice == '5':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 