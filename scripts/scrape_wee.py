
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

# Try to import email configuration
try:
    # Try to import from scripts directory first
    try:
        from email_config import (
            RECIPIENTS, EMAIL_SERVER_CONFIG, GLOBAL_ALERT_SETTINGS, 
            EMAIL_TEMPLATES, can_send_alert, record_alert_sent
        )
    except ImportError:
        # Fallback to config directory
        from config.email_config import (
            RECIPIENTS, EMAIL_SERVER_CONFIG, GLOBAL_ALERT_SETTINGS, 
            EMAIL_TEMPLATES, can_send_alert, record_alert_sent
        )
    EMAIL_ENABLED = GLOBAL_ALERT_SETTINGS.get('enable_alerts', False)
except ImportError:
    RECIPIENTS = []
    EMAIL_SERVER_CONFIG = {}
    GLOBAL_ALERT_SETTINGS = {}
    EMAIL_TEMPLATES = {}
    EMAIL_ENABLED = False
    print("⚠️ Email configuration not found. Run 'python scripts/manage_emails.py' to set up.")

# Load environment variables
import os
import json
from dotenv import load_dotenv

load_dotenv()

# 📌 Products to track for price drops - Comprehensive Indian Grocery List
tracked_products_str = os.getenv('TRACKED_PRODUCTS', '[]')
try:
    TRACKED_PRODUCTS = json.loads(tracked_products_str)
except json.JSONDecodeError:
    # Default comprehensive list of Indian grocery items to track
    TRACKED_PRODUCTS = [
        # Fresh Vegetables
        "Indian Eggplant 2 lb",
        "Indian Bitter Melon 2 lb",
        "Indian okra 0.9-1.1 lb",
        "Red onions 2 lb bag",
        "Roma tomatoes 2 lb bag",
        "Fresh ginger 0.95-1.05 lb",
        "Green onion 1 bunch",
        "Cauliflower 1 head",
        "Spinach 1 bunch",
        "Sleeved garlic pack 5 ct",
        "Green cabbage 1 head",
        "Yellow onion 3 lb bag",
        "Persian cucumbers 0.9-1.1 lb",
        "Idaho russet potatoes 5 lb",
        "Green bell pepper",
        "Opo squash 1 pc",
        "Green beans 0.9-1.1 lb",
        "Carrots 2 lb bag",
        
        # Fresh Herbs
        "Cilantro 1 bunch",
        "Curry leaves 0.25 oz",
        "Mint 1 bunch",
        
        # Fresh Fruits
        "Bananas 2.6-3 lb",
        
        # Fresh Chilies
        "Mini spicy green chilies 226 g bag",
        
        # Instant Noodles
        "Maggi Masala instant noodles 9.8 oz",
        
        # Frozen Items
        "Deep Paneer Paratha Frozen 4 pcs 13 oz",
        "Deep Bhagwati's Methi Thepla 9 oz",
        "Deep ClayOven Tandoori Naan Family Pack 42.4 oz",
        "Deep Family Pack Homestyle Paratha 20 pcs 46 oz",
        "Franco uncooked phulka 18 pcs 1.31 lb",
        
        # Rice Products
        "Laxmi Poha Flattened Rice Thick 4 lb",
        "Shastha Dosa Batter 32 oz",
        "India Gate Basmati Rice",
        "Laxmi Idli Rice 20 lb",
        "Regal Sona Masoori Rice 20 lb",
        "Laxmi Ponni Boiled Rice 20 lb",
        
        # Flour Products
        "Aashirvaad Whole Wheat Atta Flour 20 lb",
        "Laxmi Besan gram flour 2 lb",
        
        # Pulses/Lentils
        "Laxmi Toor Dal Split Pigeon Peas 4 lb",
        "Laxmi Moong Dal Skinned mung beans 4 lb",
        "Laxmi Yellow Split Peas 4 lb",
        "Laxmi Urad Dal Split 4 lb",
        "Laxmi Chana Dal 4 lb",
        "Laxmi Kabuli Chana chickpeas 4 lb",
        "Laxmi Kala Chana black chickpeas 4 lb",
        "Laxmi Urad Gota black whole lentil 4 lb",
        "Laxmi Urad Dal skinned 4 lb",
        "Laxmi Sabudana tapioca 4 lb",
        
        # Dairy Products
        "Vadilal Paneer Block",
        "Nanak Plain Paneer 400 g",
        "Pavel's whole-milk yogurt 32 oz",
        "Amul Ghee clarified butter",
        
        # Snacks
        "Garvi Gujarat Gujarati Chakri 10 oz",
        "Kurkure Masala Munch chips",
        "Kurkure Chilli Chatka chips",
        "Lay's Magic Masala chips 1.82 oz",
        "Laxmi Puffed Rice 14 oz",
        
        # Condiments/Sauces
        "Ching's Schezwan chutney",
        "Lee Kum Kee Supreme Soy Sauce 500 ml",
        
        # Spices
        "Aara Cumin Seeds",
        
        # Fish
        "TSF Barramundi Whole Cleaned 500-550 g"
    ]

# Debug: Print what products we're tracking (only in debug mode)
if os.getenv('DEBUG_MODE', 'false').lower() == 'true':
    print(f"🔍 Debug: TRACKED_PRODUCTS = {TRACKED_PRODUCTS}")

# 📌 Updated URL to a valid product category page
BASE_URL = os.getenv('BASE_URL', "https://www.sayweee.com/en/category/sale")  # Deals/Sale page

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
        # Exact match or high similarity (>0.6 for more flexible matching)
        if tracked.lower() == product_name.lower() or similar(tracked, product_name) > 0.6:
            return True
        
        # Check if key words match
        tracked_words = set(tracked.lower().split())
        product_words = set(product_name.lower().split())
        
        # If more than 40% of words match, consider it a match
        common_words = tracked_words.intersection(product_words)
        if len(common_words) >= len(tracked_words) * 0.4:
            return True
        
        # Check for specific brand/product keywords
        brand_keywords = [
            ('maggi', 'maggi'),
            ('lee kum', 'lee kum'),
            ('soy sauce', 'soy'),
            ('noodles', 'noodles'),
            ('barramundi', 'barramundi'),
            ('tsf', 'tsf'),
            ('laxmi', 'laxmi'),
            ('deep', 'deep'),
            ('aashirvaad', 'aashirvaad'),
            ('india gate', 'india gate'),
            ('regal', 'regal'),
            ('pavel', 'pavel'),
            ('amul', 'amul'),
            ('vadilal', 'vadilal'),
            ('nanak', 'nanak'),
            ('garvi gujarat', 'garvi'),
            ('kurkure', 'kurkure'),
            ('lay', 'lay'),
            ('ching', 'ching'),
            ('aara', 'aara'),
            ('shastha', 'shastha'),
            ('franco', 'franco')
        ]
        
        for tracked_keyword, product_keyword in brand_keywords:
            if tracked_keyword in tracked.lower() and product_keyword in product_name.lower():
                return True
        
        # Check for specific product type keywords
        product_type_keywords = [
            ('paneer', 'paneer'),
            ('ghee', 'ghee'),
            ('yogurt', 'yogurt'),
            ('rice', 'rice'),
            ('flour', 'flour'),
            ('atta', 'atta'),
            ('besan', 'besan'),
            ('dal', 'dal'),
            ('chana', 'chana'),
            ('urad', 'urad'),
            ('moong', 'moong'),
            ('toor', 'toor'),
            ('sabudana', 'sabudana'),
            ('poha', 'poha'),
            ('paratha', 'paratha'),
            ('naan', 'naan'),
            ('thepla', 'thepla'),
            ('phulka', 'phulka'),
            ('dosa', 'dosa'),
            ('idli', 'idli'),
            ('chakri', 'chakri'),
            ('chips', 'chips'),
            ('cumin', 'cumin'),
            ('eggplant', 'eggplant'),
            ('okra', 'okra'),
            ('onion', 'onion'),
            ('tomato', 'tomato'),
            ('ginger', 'ginger'),
            ('garlic', 'garlic'),
            ('cabbage', 'cabbage'),
            ('cucumber', 'cucumber'),
            ('potato', 'potato'),
            ('bell pepper', 'pepper'),
            ('squash', 'squash'),
            ('beans', 'beans'),
            ('carrot', 'carrot'),
            ('cilantro', 'cilantro'),
            ('curry leaves', 'curry'),
            ('mint', 'mint'),
            ('banana', 'banana'),
            ('chilies', 'chili'),
            ('chilli', 'chili')
        ]
        
        for tracked_keyword, product_keyword in product_type_keywords:
            if tracked_keyword in tracked.lower() and product_keyword in product_name.lower():
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
    """Send email alert for price drop to multiple recipients"""
    try:
        # Calculate savings
        savings_amount = old_price - new_price
        savings_percentage = (savings_amount / old_price) * 100
        
        # Always print console alert
        print(f"🚨 PRICE DROP ALERT!")
        print(f"Product: {product_name}")
        print(f"Old Price: ${old_price:.2f}")
        print(f"New Price: ${new_price:.2f}")
        print(f"Savings: ${savings_amount:.2f} ({savings_percentage:.1f}% off)")
        print("-" * 50)
        
        # Send emails to enabled recipients
        if EMAIL_ENABLED and RECIPIENTS:
            enabled_recipients = [r for r in RECIPIENTS if r['enabled']]
            
            if not enabled_recipients:
                print("📧 No enabled recipients found")
                return True
            
            emails_sent = 0
            
            for recipient in enabled_recipients:
                # Check recipient preferences
                prefs = recipient['alert_preferences']
                if (savings_amount < prefs['minimum_savings'] or 
                    savings_percentage < prefs['minimum_percentage']):
                    continue
                
                # Check if we can send alert (prevent spam)
                if not can_send_alert(product_name, recipient['email']):
                    print(f"⏰ Skipping alert to {recipient['name']} (cooldown/limit)")
                    continue
                
                try:
                    # Send email to this recipient
                    success = send_single_email(
                        product_name, old_price, new_price, 
                        savings_amount, savings_percentage, recipient
                    )
                    
                    if success:
                        record_alert_sent(product_name, recipient['email'])
                        emails_sent += 1
                        
                except Exception as e:
                    print(f"❌ Failed to send email to {recipient['name']}: {e}")
            
            if emails_sent > 0:
                print(f"📧 Sent {emails_sent} email alert(s)")
            else:
                print("📧 No email alerts sent (preferences/limits)")
        else:
            print("📧 Email alerts disabled or no recipients configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to send alert: {e}")
        return False

def send_single_email(product_name, old_price, new_price, savings_amount, savings_percentage, recipient):
    """Send email to a single recipient"""
    
    # Email configuration
    smtp_server = EMAIL_SERVER_CONFIG['smtp_server']
    smtp_port = EMAIL_SERVER_CONFIG['smtp_port']
    sender_email = EMAIL_SERVER_CONFIG['sender_email']
    sender_password = EMAIL_SERVER_CONFIG['sender_password']
    sender_name = EMAIL_SERVER_CONFIG['sender_name']
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = f"{sender_name} <{sender_email}>"
    msg['To'] = recipient['email']
    
    # Subject line
    subject_prefix = GLOBAL_ALERT_SETTINGS.get('email_subject_prefix', '🚨 Weee! Price Drop Alert: ')
    msg['Subject'] = f"{subject_prefix}{product_name}"
    
    # Email body
    product_url = BASE_URL if GLOBAL_ALERT_SETTINGS.get('include_product_link', True) else ""
    
    # Plain text version
    text_body = EMAIL_TEMPLATES['plain_text'].format(
        recipient_name=recipient['name'],
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        savings_amount=savings_amount,
        savings_percentage=savings_percentage,
        product_url=product_url
    )
    
    # HTML version
    html_body = EMAIL_TEMPLATES['html'].format(
        recipient_name=recipient['name'],
        product_name=product_name,
        old_price=old_price,
        new_price=new_price,
        savings_amount=savings_amount,
        savings_percentage=savings_percentage,
        product_url=product_url
    )
    
    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))
    
    # Send email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, recipient['email'], text)
    server.quit()
    
    print(f"✅ Email sent to {recipient['name']} ({recipient['email']})")
    return True

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
        'a[href*="/product/"]',  # Links to product pages
        'div[class*="item"]',  # Generic item containers
        'div[class*="product-item"]',  # Product items
        'div[class*="product-card"]'  # Product cards
    ]
    
    for selector in selectors_to_try:
        items = soup.select(selector)
        print(f"Selector '{selector}': found {len(items)} items")
        
        if items:
            for i, item in enumerate(items[:30]):  # Increased to 30 for more variety
                try:
                    # Try different ways to extract product name
                    name_selectors = [
                        'div[data-role="product-name"]',
                        '[data-testid*="name"]',
                        '[data-testid*="title"]',
                        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                        '.product-name',
                        '.title',
                        '.name',
                        'a[href*="/product/"]',
                        'span[class*="name"]',
                        'span[class*="title"]',
                        'div[class*="name"]',
                        'div[class*="title"]',
                        'p[class*="name"]',
                        'p[class*="title"]'
                    ]
                    
                    name = None
                    for name_sel in name_selectors:
                        name_elem = item.select_one(name_sel)
                        if name_elem:
                            name = name_elem.get_text(strip=True)
                            if name and len(name) > 3:  # Ensure it's a meaningful name
                                break
                    
                    # If no name found, try to get text from the entire item
                    if not name:
                        # Get all text from the item and look for product-like text
                        all_text = item.get_text(strip=True)
                        lines = all_text.split('\n')
                        for line in lines:
                            line = line.strip()
                            if len(line) > 10 and any(keyword in line.lower() for keyword in ['noodles', 'sauce', 'soy', 'maggi', 'lee kum', 'barramundi', 'fish']):
                                name = line
                                break
                    
                    # 🎯 Only process tracked products (but be more flexible)
                    if not name:
                        continue
                    
                    # Check if this product matches any tracked product
                    is_tracked = is_tracked_product(name)
                    
                    # Debug: Show product matching (only in debug mode)
                    if os.getenv('DEBUG_MODE', 'false').lower() == 'true' and name and len(name) > 5:
                        if is_tracked:
                            print(f"✅ Matched: '{name}'")
                        else:
                            print(f"❌ Not matched: '{name}'")
                    
                    # Debug: Print all products found (only in debug mode)
                    if os.getenv('DEBUG_MODE', 'false').lower() == 'true' and name and len(name) > 5:
                        print(f"🔍 Found product: '{name}' - Tracked: {is_tracked}")
                    
                    if not is_tracked:
                        continue
                    
                    # Try different ways to extract price
                    price_selectors = [
                        'div[data-testid="wid-product-card-price"]',
                        '[data-testid*="price"]',
                        '.price',
                        '[class*="price"]',
                        '[class*="Price"]',
                        'span[class*="price"]',
                        'div[class*="price"]',
                        'p[class*="price"]'
                    ]
                    
                    price = None
                    for price_sel in price_selectors:
                        price_elem = item.select_one(price_sel)
                        if price_elem:
                            price = price_elem.get_text(strip=True)
                            if price and ('$' in price or '€' in price or '£' in price):
                                break
                    
                    # If no price found, look for price patterns in all text
                    if not price:
                        all_text = item.get_text(strip=True)
                        price_match = re.search(r'\$[\d,]+\.?\d*', all_text)
                        if price_match:
                            price = price_match.group()
                    
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
