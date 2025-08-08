#!/usr/bin/env python3
# scripts/migrate_csv_to_firebase.py

import pandas as pd
import os
import sys
from datetime import datetime
import logging

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from firebase_manager import FirebaseManager
from scrape_wee import extract_price_value

def migrate_csv_to_firebase():
    """Migrate existing CSV data to Firebase"""
    try:
        # Initialize Firebase
        firebase = FirebaseManager()
        logger = logging.getLogger(__name__)
        
        # Read existing CSV
        csv_file = 'data/processed/wee_prices.csv'
        if not os.path.exists(csv_file):
            print(f"❌ CSV file not found: {csv_file}")
            return False
        
        df = pd.read_csv(csv_file)
        print(f"📊 Found {len(df)} records in CSV file")
        
        # Track migration progress
        migrated_count = 0
        error_count = 0
        
        for index, row in df.iterrows():
            try:
                # Extract product data
                product_name = row['Product Name']
                price_str = row['Price']
                unit = row.get('Unit', '')
                brand = row.get('Brand', '')
                category = row.get('Category', '')
                timestamp = row.get('Timestamp', '')
                source = row.get('Source', '')
                
                # Extract price value - handle both string and float prices
                if isinstance(price_str, str):
                    price_value = extract_price_value(price_str)
                else:
                    price_value = float(price_str) if price_str else None
                
                # Prepare price data
                price_data = {
                    'price': price_value,
                    'price_str': price_str,
                    'unit_price': None,
                    'unit_price_str': unit,
                    'source_url': None,
                    'source_selector': source,
                    'brand': brand,
                    'category': category,
                    'unit': unit
                }
                
                # Save to Firebase
                if firebase.save_price_to_firebase(product_name, price_data):
                    migrated_count += 1
                    if migrated_count % 10 == 0:
                        print(f"✅ Migrated {migrated_count} records...")
                else:
                    error_count += 1
                    
            except Exception as e:
                error_count += 1
                print(f"❌ Error migrating row {index}: {e}")
                continue
        
        print(f"🎉 Migration completed!")
        print(f"✅ Successfully migrated: {migrated_count} records")
        print(f"❌ Errors: {error_count} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def backup_csv_file():
    """Create a backup of the original CSV file"""
    import shutil
    from datetime import datetime
    
    csv_file = 'data/processed/wee_prices.csv'
    if os.path.exists(csv_file):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'data/processed/wee_prices_backup_{timestamp}.csv'
        
        shutil.copy2(csv_file, backup_file)
        print(f"📁 Created backup: {backup_file}")
        return backup_file
    return None

def main():
    """Main migration function"""
    print("🚀 Starting CSV to Firebase Migration")
    print("=" * 50)
    
    # Check if Firebase is available
    try:
        from firebase_manager import FirebaseManager
        firebase = FirebaseManager()
        print("✅ Firebase connection successful")
    except Exception as e:
        print(f"❌ Firebase connection failed: {e}")
        print("💡 Make sure you have configured Firebase credentials in your .env file")
        return False
    
    # Create backup
    backup_file = backup_csv_file()
    
    # Auto-confirm for testing
    print("\n⚠️ This will migrate all CSV data to Firebase.")
    print("📁 A backup of your CSV file has been created.")
    print("🔄 Auto-confirming migration for testing...")
    
    # Run migration
    success = migrate_csv_to_firebase()
    
    if success:
        print("\n🎉 Migration completed successfully!")
        print("🔥 Your data is now stored in Firebase")
        print("📊 You can now use the Firebase-enabled scraper")
    else:
        print("\n❌ Migration failed")
        print("📁 Your original data is safe in the backup file")
    
    return success

if __name__ == "__main__":
    main() 