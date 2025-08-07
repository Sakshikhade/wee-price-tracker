#!/usr/bin/env python3
# scripts/env_loader.py - Environment variable loader

import os
import json
from pathlib import Path
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file"""
    
    # Load .env file
    env_file = Path('.env')
    if env_file.exists():
        load_dotenv(env_file)
        print("✅ Environment variables loaded from .env file")
    else:
        print("⚠️ .env file not found, using default values")
    
    # Email Server Configuration
    email_config = {
        'smtp_server': os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('EMAIL_SMTP_PORT', '587')),
        'sender_email': os.getenv('EMAIL_SENDER_ADDRESS', 'your_email@gmail.com'),
        'sender_password': os.getenv('EMAIL_SENDER_PASSWORD', 'your_app_password'),
        'sender_name': os.getenv('EMAIL_SENDER_NAME', 'Weee! Price Tracker')
    }
    
    # Global Alert Settings
    alert_settings = {
        'enable_alerts': os.getenv('EMAIL_ENABLE_ALERTS', 'true').lower() == 'true',
        'include_product_link': True,
        'email_subject_prefix': os.getenv('EMAIL_SUBJECT_PREFIX', '🚨 Weee! Price Drop Alert: '),
        'max_alerts_per_day': int(os.getenv('EMAIL_MAX_ALERTS_PER_DAY', '5')),
        'alert_cooldown_hours': int(os.getenv('EMAIL_ALERT_COOLDOWN_HOURS', '6'))
    }
    
    # Product Tracking
    tracked_products_str = os.getenv('TRACKED_PRODUCTS', '["Maggi Masala Instant Noodles 9.8 oz", "Lee Kum Kee Supreme Soy Sauce 500 ml"]')
    try:
        tracked_products = json.loads(tracked_products_str)
    except json.JSONDecodeError:
        tracked_products = ["Maggi Masala Instant Noodles 9.8 oz", "Lee Kum Kee Supreme Soy Sauce 500 ml"]
    
    # Web Scraping
    scraping_config = {
        'base_url': os.getenv('BASE_URL', 'https://www.sayweee.com/en/category/sale'),
        'request_timeout': int(os.getenv('REQUEST_TIMEOUT', '10')),
        'max_retries': int(os.getenv('MAX_RETRIES', '3'))
    }
    
    # Data Storage
    data_config = {
        'data_dir': os.getenv('DATA_DIR', 'data/processed'),
        'price_history_file': os.getenv('PRICE_HISTORY_FILE', 'price_history.json'),
        'alert_history_file': os.getenv('ALERT_HISTORY_FILE', 'alert_history.json'),
        'csv_output_file': os.getenv('CSV_OUTPUT_FILE', 'wee_prices.csv')
    }
    
    # Logging
    logging_config = {
        'log_level': os.getenv('LOG_LEVEL', 'INFO'),
        'log_file': os.getenv('LOG_FILE', 'logs/price_tracker.log')
    }
    
    # Scheduler
    scheduler_config = {
        'run_time': os.getenv('SCHEDULER_RUN_TIME', '09:00'),
        'enabled': os.getenv('SCHEDULER_ENABLED', 'true').lower() == 'true'
    }
    
    # Development
    dev_config = {
        'debug_mode': os.getenv('DEBUG_MODE', 'false').lower() == 'true',
        'test_mode': os.getenv('TEST_MODE', 'false').lower() == 'true'
    }
    
    return {
        'email_config': email_config,
        'alert_settings': alert_settings,
        'tracked_products': tracked_products,
        'scraping_config': scraping_config,
        'data_config': data_config,
        'logging_config': logging_config,
        'scheduler_config': scheduler_config,
        'dev_config': dev_config
    }

def create_env_template():
    """Create a template .env file"""
    
    template_content = """# Weee! Price Tracker - Environment Variables
# Copy this file to .env and fill in your actual values

# Email Server Configuration
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER_ADDRESS=your_email@gmail.com
EMAIL_SENDER_PASSWORD=your_app_password
EMAIL_SENDER_NAME=Weee! Price Tracker

# Email Alert Settings
EMAIL_ENABLE_ALERTS=true
EMAIL_MAX_ALERTS_PER_DAY=5
EMAIL_ALERT_COOLDOWN_HOURS=6
EMAIL_SUBJECT_PREFIX=🚨 Weee! Price Drop Alert: 

# Product Tracking
TRACKED_PRODUCTS=["Maggi Masala Instant Noodles 9.8 oz", "Lee Kum Kee Supreme Soy Sauce 500 ml"]

# Web Scraping
BASE_URL=https://www.sayweee.com/en/category/sale
REQUEST_TIMEOUT=10
MAX_RETRIES=3

# Data Storage
DATA_DIR=data/processed
PRICE_HISTORY_FILE=price_history.json
ALERT_HISTORY_FILE=alert_history.json
CSV_OUTPUT_FILE=wee_prices.csv

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/price_tracker.log

# Scheduler Settings
SCHEDULER_RUN_TIME=09:00
SCHEDULER_ENABLED=true

# Development/Testing
DEBUG_MODE=false
TEST_MODE=false
"""
    
    with open('.env.template', 'w') as f:
        f.write(template_content)
    
    print("✅ Created .env.template file")

def validate_env_config():
    """Validate environment configuration"""
    
    config = load_environment()
    
    print("🔍 Validating Environment Configuration")
    print("=" * 40)
    
    # Check email configuration
    email_config = config['email_config']
    print(f"📧 SMTP Server: {email_config['smtp_server']}:{email_config['smtp_port']}")
    print(f"📧 Sender Email: {email_config['sender_email']}")
    print(f"📧 Sender Name: {email_config['sender_name']}")
    
    if email_config['sender_password'] == 'your_app_password':
        print("⚠️ Warning: Using default app password")
    else:
        print("✅ App password configured")
    
    # Check alert settings
    alert_settings = config['alert_settings']
    print(f"🔔 Alerts Enabled: {alert_settings['enable_alerts']}")
    print(f"🔔 Max Alerts/Day: {alert_settings['max_alerts_per_day']}")
    print(f"🔔 Cooldown Hours: {alert_settings['alert_cooldown_hours']}")
    
    # Check tracked products
    tracked_products = config['tracked_products']
    print(f"🛍️ Tracked Products: {len(tracked_products)}")
    for i, product in enumerate(tracked_products, 1):
        print(f"  {i}. {product}")
    
    # Check data configuration
    data_config = config['data_config']
    print(f"📁 Data Directory: {data_config['data_dir']}")
    print(f"📁 Price History: {data_config['price_history_file']}")
    print(f"📁 Alert History: {data_config['alert_history_file']}")
    
    # Check scheduler
    scheduler_config = config['scheduler_config']
    print(f"⏰ Scheduler Enabled: {scheduler_config['enabled']}")
    print(f"⏰ Run Time: {scheduler_config['run_time']}")
    
    # Check development settings
    dev_config = config['dev_config']
    print(f"🐛 Debug Mode: {dev_config['debug_mode']}")
    print(f"🧪 Test Mode: {dev_config['test_mode']}")
    
    print("\n✅ Environment validation complete!")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "template":
            create_env_template()
        elif command == "validate":
            validate_env_config()
        elif command == "load":
            config = load_environment()
            print("Configuration loaded successfully")
        else:
            print("❌ Unknown command. Use: template, validate, or load")
    else:
        print("Environment Loader Options:")
        print("1. Create template: python scripts/env_loader.py template")
        print("2. Validate config: python scripts/env_loader.py validate")
        print("3. Load config: python scripts/env_loader.py load")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            create_env_template()
        elif choice == "2":
            validate_env_config()
        elif choice == "3":
            config = load_environment()
            print("Configuration loaded successfully")
        else:
            print("❌ Invalid choice") 