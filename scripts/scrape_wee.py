
# scripts/scrape_wee.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import json
from difflib import SequenceMatcher

# 📌 Products to track for price drops
TRACKED_PRODUCTS = [
    "Maggi Masala Instant Noodles 9.8 oz",
    "Lee Kum Kee Supreme Soy Sauce 500 ml"
]

# 📌 Updated URL to a valid product category page
BASE_URL = "https://www.sayweee.com/en/category/sale"  # Deals/Sale page

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def similar(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def is_tracked_product(product_name):
    """Check if a product name matches any tracked product (with fuzzy matching)"""
    if not product_name:
        return False
    
    for tracked in TRACKED_PRODUCTS:
        # Exact match or high similarity (>0.8)
        if tracked.lower() == product_name.lower() or similar(tracked, product_name) > 0.8:
            return True
    return False

def extract_price_value(price_str):
    """Extract numeric price value from price string"""
    if not price_str:
        return None
    
    # Remove currency symbols and extract number
    price_match = re.search(r'[\d,]+\.?\d*', price_str.replace(',', ''))
    if price_match:
        try:
            return float(price_match.group())
        except ValueError:
            return None
    return None

def load_price_history(filename="data/processed/price_history.json"):
    """Load historical price data"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    return {}

def save_price_history(history, filename="data/processed/price_history.json"):
    """Save historical price data"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(history, f, indent=2)

def send_price_alert(product_name, old_price, new_price, email_config=None):
    """Send email alert for price drop"""
    try:
        if not email_config:
            # Print alert if no email config
            print(f"🚨 PRICE DROP ALERT!")
            print(f"Product: {product_name}")
            print(f"Old Price: ${old_price:.2f}")
            print(f"New Price: ${new_price:.2f}")
            print(f"Savings: ${old_price - new_price:.2f} ({((old_price - new_price) / old_price * 100):.1f}% off)")
            print("-" * 50)
            return True
            
        # Email configuration (if provided)
        smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = email_config.get('smtp_port', 587)
        sender_email = email_config['sakshukhade@gmail.com']
        sender_password = email_config['Sak@Gmail']
        recipient_email = email_config['skhade5@asu.edu']
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"🚨 Price Drop Alert: {product_name}"
        
        body = f"""
        Great news! The price for one of your tracked products has dropped!
        
        Product: {product_name}
        Old Price: ${old_price:.2f}
        New Price: ${new_price:.2f}
        You Save: ${old_price - new_price:.2f} ({((old_price - new_price) / old_price * 100):.1f}% off)
        
        Check it out at: {BASE_URL}
        
        Happy shopping!
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"✅ Price drop alert sent for {product_name}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")
        return False

def check_price_drops(products):
    """Check for price drops and send alerts"""
    if not products:
        return
    
    history = load_price_history()
    alerts_sent = 0
    
    for product in products:
        name = product['Product Name']
        price_str = product['Price']
        current_price = extract_price_value(price_str)
        
        if not current_price:
            continue
            
        # Check if we have historical data for this product
        if name in history:
            last_price = history[name].get('price')
            if last_price and current_price < last_price:
                # Price dropped!
                send_price_alert(name, last_price, current_price)
                alerts_sent += 1
        
        # Update price history
        history[name] = {
            'price': current_price,
            'timestamp': product['Timestamp'],
            'price_str': price_str
        }
    
    # Save updated history
    save_price_history(history)
    
    if alerts_sent > 0:
        print(f"📧 Sent {alerts_sent} price drop alert(s)")
    else:
        print("💰 No price drops detected for tracked products")

def fetch_html(url):
    try:
        print(f"Fetching URL: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Response status: {response.status_code}")
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

def parse_product_data(html):
    if not html:
        return []
        
    soup = BeautifulSoup(html, "html.parser")
    products = []
    seen_products = set()  # To avoid duplicates
    
    print("🔍 Looking for product containers...")
    
    # Try multiple selectors that might contain product information
    selectors_to_try = [
        'div[data-testid="wid-product-card-container"]',  # Original selector
        '[data-testid*="product"]',  # Any element with product in data-testid
        '.product-card',
        '.product-item',
        'article',
        '[class*="product"]',
        '[class*="Product"]',
        'div[class*="card"]',
        'a[href*="/product/"]'  # Links to product pages
    ]
    
    for selector in selectors_to_try:
        items = soup.select(selector)
        print(f"Selector '{selector}': found {len(items)} items")
        
        if items:
            for i, item in enumerate(items[:20]):  # Increased to 20 for more variety
                try:
                    # Try different ways to extract product name
                    name_selectors = [
                        'div[data-role="product-name"]',
                        '[data-testid*="name"]',
                        'h1', 'h2', 'h3', 'h4',
                        '.product-name',
                        '.title',
                        'a[href*="/product/"]'
                    ]
                    
                    name = None
                    for name_sel in name_selectors:
                        name_elem = item.select_one(name_sel)
                        if name_elem:
                            name = name_elem.get_text(strip=True)
                            break
                    
                    # 🎯 Only process tracked products
                    if not name or not is_tracked_product(name):
                        continue
                    
                    # Try different ways to extract price
                    price_selectors = [
                        'div[data-testid="wid-product-card-price"]',
                        '[data-testid*="price"]',
                        '.price',
                        '[class*="price"]',
                        '[class*="Price"]'
                    ]
                    
                    price = None
                    for price_sel in price_selectors:
                        price_elem = item.select_one(price_sel)
                        if price_elem:
                            price = price_elem.get_text(strip=True)
                            break
                    
                    # Try to extract unit price
                    unit_price_selectors = [
                        'div[data-role="product-unit-price"]',
                        '[data-testid*="unit"]',
                        '.unit-price',
                        '.unit'
                    ]
                    
                    unit_price = None
                    for unit_sel in unit_price_selectors:
                        unit_elem = item.select_one(unit_sel)
                        if unit_elem:
                            unit_price = unit_elem.get_text(strip=True)
                            break
                    
                    # Create a unique identifier for the product
                    product_id = f"{name}_{price}"
                    
                    # If we found at least a name or price, and it's not a duplicate
                    if (name or price) and product_id not in seen_products:
                        seen_products.add(product_id)
                        product = {
                            "Product Name": name or "N/A",
                            "Price": price or "N/A",
                            "Unit": unit_price or "",
                            "Brand": "",
                            "Category": "",
                            "Timestamp": datetime.now().isoformat(),
                            "Source": selector  # Track which selector worked
                        }
                        products.append(product)
                        print(f"✅ Found product {len(products)}: {name} - {price}")
                        
                except Exception as e:
                    print(f"⚠️ Error parsing item {i+1}: {e}")
                    continue
            
            if products:
                break  # If we found products with this selector, stop trying others
    
    print(f"📊 Total unique products found: {len(products)}")
    return products


def save_to_csv(products, filename="data/processed/wee_prices.csv"):
    if not products:
        print("⚠️ No products to save")
        return
        
    df = pd.DataFrame(products)

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    # Check if file exists to avoid writing headers again
    write_header = not os.path.exists(filename)
    df.to_csv(filename, mode='a', index=False, header=write_header)
    print(f"✅ Saved {len(products)} products to {filename}")

if __name__ == "__main__":
    print("🚀 Starting Weee! price tracker...")
    print(f"📋 Tracking {len(TRACKED_PRODUCTS)} products:")
    for i, product in enumerate(TRACKED_PRODUCTS, 1):
        print(f"  {i}. {product}")
    print()
    
    html = fetch_html(BASE_URL)
    
    if html:
        print("📄 HTML fetched successfully, parsing products...")
        product_data = parse_product_data(html)

        if product_data:
            print(f"✅ Found {len(product_data)} tracked products")
            save_to_csv(product_data)
            check_price_drops(product_data)
        else:
            print("⚠️ No tracked products found on this page.")
            print("💡 The products might be out of stock or on different pages.")
    else:
        print("❌ Failed to fetch HTML. Check your internet connection and the URL.")
