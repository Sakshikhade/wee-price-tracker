#!/usr/bin/env python3
# scripts/setup_email_alerts.py - Quick email alert setup

import os
import sys

def create_initial_config():
    """Create initial email configuration"""
    
    print("📧 Weee! Price Tracker - Email Alert Setup")
    print("=" * 50)
    
    # Create config directory
    os.makedirs('config', exist_ok=True)
    
    print("🔧 Step 1: Email Server Configuration")
    print("-" * 40)
    
    sender_email = input("Enter your Gmail address: ").strip()
    if not sender_email:
        print("❌ Email address is required")
        return False
    
    sender_password = input("Enter your Gmail app password: ").strip()
    if not sender_password:
        print("❌ App password is required")
        return False
    
    sender_name = input("Enter sender name (Weee! Price Tracker): ").strip() or "Weee! Price Tracker"
    
    print("\n👥 Step 2: Add Recipients")
    print("-" * 30)
    
    recipients = []
    while True:
        add_another = input("\nAdd a recipient? (y/N): ").strip().lower()
        if add_another != 'y':
            break
        
        name = input("Recipient name: ").strip()
        email = input("Recipient email: ").strip()
        
        if not name or not email:
            print("❌ Name and email are required")
            continue
        
        print("\n📊 Alert Preferences:")
        min_savings = float(input("Minimum savings amount ($) [1.00]: ") or "1.00")
        min_percentage = float(input("Minimum percentage drop (%) [5.0]: ") or "5.0")
        
        print("\n⏰ Alert Frequency:")
        print("1. Immediate")
        print("2. Daily")
        print("3. Weekly")
        freq_choice = input("Choice (1-3) [1]: ").strip() or "1"
        frequency_map = {"1": "immediate", "2": "daily", "3": "weekly"}
        frequency = frequency_map.get(freq_choice, "immediate")
        
        recipient = {
            'email': email,
            'name': name,
            'enabled': True,
            'alert_preferences': {
                'minimum_savings': min_savings,
                'minimum_percentage': min_percentage,
                'alert_frequency': frequency
            }
        }
        
        recipients.append(recipient)
        print(f"✅ Added {name} ({email})")
    
    if not recipients:
        print("❌ At least one recipient is required")
        return False
    
    # Create the configuration
    config_content = f'''# config/email_config.py - Advanced multi-recipient email configuration

import json
import os
from datetime import datetime

# Email Server Configuration
EMAIL_SERVER_CONFIG = {{
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': '{sender_email}',
    'sender_password': '{sender_password}',
    'sender_name': '{sender_name}'
}}

# Recipients Configuration
RECIPIENTS = {json.dumps(recipients, indent=4)}

# Global Alert Settings
GLOBAL_ALERT_SETTINGS = {{
    'enable_alerts': True,
    'include_product_link': True,
    'email_subject_prefix': '🚨 Weee! Price Drop Alert: ',
    'max_alerts_per_day': 5,
    'alert_cooldown_hours': 6
}}

# Email Templates
EMAIL_TEMPLATES = {{
    'subject': '🚨 Price Drop Alert: {{product_name}}',
    'plain_text': '''
Dear {{recipient_name}},

Great news! The price for one of your tracked products has dropped!

Product: {{product_name}}
Old Price: ${{old_price:.2f}}
New Price: ${{new_price:.2f}}
You Save: ${{savings_amount:.2f}} ({{savings_percentage:.1f}}% off)

Check it out at: {{product_url}}

Best regards,
Your Weee! Price Tracker
    ''',
    'html': '''
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
        <h2 style="color: #28a745;">🚨 Price Drop Alert!</h2>
        <p>Dear {{recipient_name}},</p>
        <p>Great news! The price for one of your tracked products has dropped!</p>
        
        <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>Product:</strong> {{product_name}}</p>
            <p><strong>Old Price:</strong> <span style="text-decoration: line-through; color: red;">${{old_price:.2f}}</span></p>
            <p><strong>New Price:</strong> <span style="color: green; font-weight: bold;">${{new_price:.2f}}</span></p>
            <p><strong>You Save:</strong> <span style="color: green; font-weight: bold;">${{savings_amount:.2f}} ({{savings_percentage:.1f}}% off)</span></p>
        </div>
        
        <div style="text-align: center; margin: 20px 0;">
            <a href="{{product_url}}" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Check it out!</a>
        </div>
        
        <p>Best regards,<br>Your Weee! Price Tracker</p>
    </div>
</body>
</html>
    '''
}}

# Alert History Tracking
ALERT_HISTORY_FILE = "data/processed/alert_history.json"

def load_alert_history():
    """Load alert history to prevent spam"""
    if os.path.exists(ALERT_HISTORY_FILE):
        try:
            with open(ALERT_HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {{}}
    return {{}}

def save_alert_history(history):
    """Save alert history"""
    os.makedirs(os.path.dirname(ALERT_HISTORY_FILE), exist_ok=True)
    with open(ALERT_HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def can_send_alert(product_name, recipient_email):
    """Check if we can send an alert (prevent spam)"""
    history = load_alert_history()
    now = datetime.now().isoformat()
    
    # Clean old entries (older than 24 hours)
    history = {{k: v for k, v in history.items() 
              if (datetime.now() - datetime.fromisoformat(v['timestamp'])).total_seconds() < 86400}}
    
    # Check if we've sent too many alerts today
    today_alerts = sum(1 for v in history.values() 
                      if v['recipient'] == recipient_email and 
                      (datetime.now() - datetime.fromisoformat(v['timestamp'])).total_seconds() < 86400)
    
    if today_alerts >= GLOBAL_ALERT_SETTINGS['max_alerts_per_day']:
        return False
    
    # Check cooldown for this specific product
    product_key = f"{{product_name}}_{{recipient_email}}"
    if product_key in history:
        last_alert = datetime.fromisoformat(history[product_key]['timestamp'])
        hours_since_last = (datetime.now() - last_alert).total_seconds() / 3600
        if hours_since_last < GLOBAL_ALERT_SETTINGS['alert_cooldown_hours']:
            return False
    
    return True

def record_alert_sent(product_name, recipient_email):
    """Record that an alert was sent"""
    history = load_alert_history()
    now = datetime.now().isoformat()
    
    product_key = f"{{product_name}}_{{recipient_email}}"
    history[product_key] = {{
        'product_name': product_name,
        'recipient': recipient_email,
        'timestamp': now
    }}
    
    save_alert_history(history)
'''
    
    with open('config/email_config.py', 'w') as f:
        f.write(config_content)
    
    print(f"\n✅ Email configuration created successfully!")
    print(f"📁 Config file: config/email_config.py")
    print(f"📧 Recipients: {len(recipients)}")
    
    return True

def show_gmail_setup():
    """Show Gmail app password setup instructions"""
    
    print("\n📧 Gmail App Password Setup:")
    print("=" * 40)
    print("1. Go to your Google Account settings")
    print("2. Enable 2-Step Verification if not already enabled")
    print("3. Go to Security → App passwords")
    print("4. Generate a new app password for 'Mail'")
    print("5. Use this 16-character password in your email config")
    print("6. Never use your regular Gmail password!")
    print("\n🔗 Gmail App Passwords: https://support.google.com/accounts/answer/185833")

def test_configuration():
    """Test the email configuration"""
    
    print("\n🧪 Testing Email Configuration")
    print("-" * 40)
    
    try:
        from config.email_config import RECIPIENTS, EMAIL_SERVER_CONFIG, GLOBAL_ALERT_SETTINGS
        print("✅ Email config loaded successfully")
        
        enabled_recipients = [r for r in RECIPIENTS if r['enabled']]
        print(f"📧 {len(enabled_recipients)} enabled recipients")
        
        for recipient in enabled_recipients:
            print(f"  - {recipient['name']} ({recipient['email']})")
        
        print(f"\n🔧 Server: {EMAIL_SERVER_CONFIG['smtp_server']}:{EMAIL_SERVER_CONFIG['smtp_port']}")
        print(f"📧 Sender: {EMAIL_SERVER_CONFIG['sender_email']}")
        
        # Test SMTP connection
        import smtplib
        server = smtplib.SMTP(EMAIL_SERVER_CONFIG['smtp_server'], EMAIL_SERVER_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_SERVER_CONFIG['sender_email'], EMAIL_SERVER_CONFIG['sender_password'])
        server.quit()
        print("✅ SMTP connection test successful!")
        print("🎉 Email alerts are ready to use!")
        
    except ImportError:
        print("❌ Email config not found. Run setup first.")
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        print("💡 Check your Gmail app password and try again")

def main():
    """Main setup function"""
    
    print("📧 Weee! Price Tracker - Email Alert Setup")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "setup":
            if create_initial_config():
                test_configuration()
        elif command == "test":
            test_configuration()
        elif command == "help":
            show_gmail_setup()
        else:
            print("❌ Unknown command. Use: setup, test, or help")
    else:
        print("Choose an option:")
        print("1. Setup email alerts")
        print("2. Test email configuration")
        print("3. Show Gmail setup instructions")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            if create_initial_config():
                test_configuration()
        elif choice == "2":
            test_configuration()
        elif choice == "3":
            show_gmail_setup()
        elif choice == "4":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main() 