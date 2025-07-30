# scripts/analyze_data.py

import pandas as pd
import os

def analyze_scraped_data():
    csv_file = "data/processed/wee_prices.csv"
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return
    
    df = pd.read_csv(csv_file)
    
    print("📊 Weee! Price Tracker - Data Analysis")
    print("=" * 50)
    print(f"Total records: {len(df)}")
    print(f"Unique products: {df['Product Name'].nunique()}")
    print(f"Date range: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
    print()
    
    print("🛍️ Product Summary:")
    print("-" * 30)
    unique_products = df.drop_duplicates(subset=['Product Name'])
    for _, product in unique_products.iterrows():
        print(f"• {product['Product Name']}")
        print(f"  Price: {product['Price']}")
        if product['Unit'] and pd.notna(product['Unit']):
            print(f"  Unit Price: {product['Unit']}")
        print()
    
    print("💰 Price Analysis:")
    print("-" * 30)
    # Extract numeric prices for analysis
    df['Price_Numeric'] = df['Price'].str.replace('$', '').str.replace(',', '').astype(float, errors='ignore')
    numeric_prices = df['Price_Numeric'].dropna()
    
    if len(numeric_prices) > 0:
        print(f"Average price: ${numeric_prices.mean():.2f}")
        print(f"Median price: ${numeric_prices.median():.2f}")
        print(f"Price range: ${numeric_prices.min():.2f} - ${numeric_prices.max():.2f}")
    
    print("\n✨ Latest scrape summary:")
    print("-" * 30)
    latest_scrape = df[df['Timestamp'] == df['Timestamp'].max()]
    print(f"Products found in latest scrape: {len(latest_scrape)}")
    print(f"Total value of products: ${latest_scrape['Price_Numeric'].sum():.2f}")

if __name__ == "__main__":
    analyze_scraped_data()
