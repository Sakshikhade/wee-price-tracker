#!/usr/bin/env python3
# scripts/manage_emails.py - Email recipient management system

import json
import os
import sys
from datetime import datetime

def load_email_config():
    """Load email configuration"""
    try:
        # Try to import from scripts directory first
        from email_config import RECIPIENTS, EMAIL_SERVER_CONFIG
        return RECIPIENTS, EMAIL_SERVER_CONFIG
    except ImportError:
        try:
            # Fallback to config directory
            from config.email_config import RECIPIENTS, EMAIL_SERVER_CONFIG
            return RECIPIENTS, EMAIL_SERVER_CONFIG
        except ImportError:
            print("❌ Email config not found. Run setup first.")
            return [], {}

def save_email_config(recipients, server_config):
    """Save email configuration"""
    # Create a simple config file
    config_lines = [
        "# config/email_config.py - Email configuration",
        "",
        "import json",
        "import os",
        "from datetime import datetime",
        "",
        "# Email Server Configuration",
        f"EMAIL_SERVER_CONFIG = {json.dumps(server_config, indent=4)}",
        "",
        "# Recipients Configuration", 
        f"RECIPIENTS = {json.dumps(recipients, indent=4)}",
        "",
        "# Global Alert Settings",
        "GLOBAL_ALERT_SETTINGS = {",
        "    'enable_alerts': True,",
        "    'include_product_link': True,",
        "    'email_subject_prefix': 'Price Drop Alert: ',",
        "    'max_alerts_per_day': 5,",
        "    'alert_cooldown_hours': 6",
        "}",
        "",
        "# Email Templates",
        "EMAIL_TEMPLATES = {",
        "    'subject': 'Price Drop Alert: {product_name}',",
        "    'plain_text': '''",
        "Dear {recipient_name},",
        "",
        "Great news! The price for one of your tracked products has dropped!",
        "",
        "Product: {product_name}",
        "Old Price: ${old_price}",
        "New Price: ${new_price}",
        "You Save: ${savings_amount} ({savings_percentage}% off)",
        "",
        "Check it out at: {product_url}",
        "",
        "Best regards,",
        "Your Weee! Price Tracker",
        "    ''',",
        "    'html': '''",
        "<html>",
        "<body style=\"font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;\">",
        "    <div style=\"background-color: #f8f9fa; padding: 20px; border-radius: 10px;\">",
        "        <h2 style=\"color: #28a745;\">Price Drop Alert!</h2>",
        "        <p>Dear {recipient_name},</p>",
        "        <p>Great news! The price for one of your tracked products has dropped!</p>",
        "        ",
        "        <div style=\"background-color: white; padding: 15px; border-radius: 5px; margin: 20px 0;\">",
        "            <p><strong>Product:</strong> {product_name}</p>",
        "            <p><strong>Old Price:</strong> <span style=\"text-decoration: line-through; color: red;\">${old_price}</span></p>",
        "            <p><strong>New Price:</strong> <span style=\"color: green; font-weight: bold;\">${new_price}</span></p>",
        "            <p><strong>You Save:</strong> <span style=\"color: green; font-weight: bold;\">${savings_amount} ({savings_percentage}% off)</span></p>",
        "        </div>",
        "        ",
        "        <div style=\"text-align: center; margin: 20px 0;\">",
        "            <a href=\"{product_url}\" style=\"background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;\">Check it out!</a>",
        "        </div>",
        "        ",
        "        <p>Best regards,<br>Your Weee! Price Tracker</p>",
        "    </div>",
        "</body>",
        "</html>",
        "    '''",
        "}",
        "",
        "# Alert History Tracking",
        "ALERT_HISTORY_FILE = \"data/processed/alert_history.json\"",
        "",
        "def load_alert_history():",
        "    \"\"\"Load alert history to prevent spam\"\"\"",
        "    if os.path.exists(ALERT_HISTORY_FILE):",
        "        try:",
        "            with open(ALERT_HISTORY_FILE, 'r') as f:",
        "                return json.load(f)",
        "        except:",
        "            return {}",
        "    return {}",
        "",
        "def save_alert_history(history):",
        "    \"\"\"Save alert history\"\"\"",
        "    os.makedirs(os.path.dirname(ALERT_HISTORY_FILE), exist_ok=True)",
        "    with open(ALERT_HISTORY_FILE, 'w') as f:",
        "        json.dump(history, f, indent=2)",
        "",
        "def can_send_alert(product_name, recipient_email):",
        "    \"\"\"Check if we can send an alert (prevent spam)\"\"\"",
        "    history = load_alert_history()",
        "    now = datetime.now().isoformat()",
        "    ",
        "    # Clean old entries (older than 24 hours)",
        "    history = {k: v for k, v in history.items()",
        "              if (datetime.now() - datetime.fromisoformat(v['timestamp'])).total_seconds() < 86400}",
        "    ",
        "    # Check if we've sent too many alerts today",
        "    today_alerts = sum(1 for v in history.values()",
        "                      if v['recipient'] == recipient_email and",
        "                      (datetime.now() - datetime.fromisoformat(v['timestamp'])).total_seconds() < 86400)",
        "    ",
        "    if today_alerts >= GLOBAL_ALERT_SETTINGS['max_alerts_per_day']:",
        "        return False",
        "    ",
        "    # Check cooldown for this specific product",
        "    product_key = f\"{product_name}_{recipient_email}\"",
        "    if product_key in history:",
        "        last_alert = datetime.fromisoformat(history[product_key]['timestamp'])",
        "        hours_since_last = (datetime.now() - last_alert).total_seconds() / 3600",
        "        if hours_since_last < GLOBAL_ALERT_SETTINGS['alert_cooldown_hours']:",
        "            return False",
        "    ",
        "    return True",
        "",
        "def record_alert_sent(product_name, recipient_email):",
        "    \"\"\"Record that an alert was sent\"\"\"",
        "    history = load_alert_history()",
        "    now = datetime.now().isoformat()",
        "    ",
        "    product_key = f\"{product_name}_{recipient_email}\"",
        "    history[product_key] = {",
        "        'product_name': product_name,",
        "        'recipient': recipient_email,",
        "        'timestamp': now",
        "    }",
        "    ",
        "    save_alert_history(history)",
        ""
    ]
    
    # Save to scripts directory
    with open('scripts/email_config.py', 'w') as f:
        f.write('\n'.join(config_lines))

def show_recipients(recipients):
    """Display current recipients"""
    print("\n📧 Current Email Recipients:")
    print("=" * 50)
    
    if not recipients:
        print("❌ No recipients configured")
        return
    
    for i, recipient in enumerate(recipients, 1):
        status = "✅ Enabled" if recipient['enabled'] else "❌ Disabled"
        print(f"{i}. {recipient['name']} ({recipient['email']}) - {status}")
        if recipient['enabled']:
            prefs = recipient['alert_preferences']
            print(f"   💰 Min savings: ${prefs['minimum_savings']:.2f}")
            print(f"   📊 Min percentage: {prefs['minimum_percentage']:.1f}%")
            print(f"   ⏰ Frequency: {prefs['alert_frequency']}")
        print()

def add_recipient(recipients):
    """Add a new recipient"""
    print("\n➕ Add New Recipient")
    print("-" * 30)
    
    name = input("Name: ").strip()
    if not name:
        print("❌ Name is required")
        return recipients
    
    email = input("Email: ").strip()
    if not email or '@' not in email:
        print("❌ Valid email is required")
        return recipients
    
    # Check if email already exists
    if any(r['email'] == email for r in recipients):
        print("❌ Email already exists")
        return recipients
    
    print("\n📊 Alert Preferences:")
    try:
        min_savings = float(input("Minimum savings amount ($): ") or "1.00")
        min_percentage = float(input("Minimum percentage drop (%): ") or "5.0")
        frequency = input("Alert frequency (immediate/daily/weekly): ").strip() or "immediate"
        
        if frequency not in ['immediate', 'daily', 'weekly']:
            frequency = 'immediate'
    except ValueError:
        print("❌ Invalid input, using defaults")
        min_savings = 1.00
        min_percentage = 5.0
        frequency = 'immediate'
    
    new_recipient = {
        'email': email,
        'name': name,
        'enabled': True,
        'alert_preferences': {
            'minimum_savings': min_savings,
            'minimum_percentage': min_percentage,
            'alert_frequency': frequency
        }
    }
    
    recipients.append(new_recipient)
    print(f"✅ Added {name} ({email})")
    return recipients

def remove_recipient(recipients):
    """Remove a recipient"""
    if not recipients:
        print("❌ No recipients to remove")
        return recipients
    
    show_recipients(recipients)
    
    try:
        choice = int(input("\nEnter recipient number to remove: ")) - 1
        if 0 <= choice < len(recipients):
            removed = recipients.pop(choice)
            print(f"✅ Removed {removed['name']} ({removed['email']})")
        else:
            print("❌ Invalid choice")
    except ValueError:
        print("❌ Invalid input")
    
    return recipients

def toggle_recipient(recipients):
    """Enable/disable a recipient"""
    if not recipients:
        print("❌ No recipients to toggle")
        return recipients
    
    show_recipients(recipients)
    
    try:
        choice = int(input("\nEnter recipient number to toggle: ")) - 1
        if 0 <= choice < len(recipients):
            recipient = recipients[choice]
            recipient['enabled'] = not recipient['enabled']
            status = "enabled" if recipient['enabled'] else "disabled"
            print(f"✅ {recipient['name']} is now {status}")
        else:
            print("❌ Invalid choice")
    except ValueError:
        print("❌ Invalid input")
    
    return recipients

def edit_recipient(recipients):
    """Edit a recipient's preferences"""
    if not recipients:
        print("❌ No recipients to edit")
        return recipients
    
    show_recipients(recipients)
    
    try:
        choice = int(input("\nEnter recipient number to edit: ")) - 1
        if 0 <= choice < len(recipients):
            recipient = recipients[choice]
            print(f"\n✏️ Editing {recipient['name']} ({recipient['email']})")
            print("-" * 40)
            
            print("📊 Alert Preferences (press Enter to keep current):")
            try:
                min_savings = input(f"Minimum savings amount (current: ${recipient['alert_preferences']['minimum_savings']:.2f}): ").strip()
                if min_savings:
                    recipient['alert_preferences']['minimum_savings'] = float(min_savings)
                
                min_percentage = input(f"Minimum percentage drop (current: {recipient['alert_preferences']['minimum_percentage']:.1f}%): ").strip()
                if min_percentage:
                    recipient['alert_preferences']['minimum_percentage'] = float(min_percentage)
                
                frequency = input(f"Alert frequency (current: {recipient['alert_preferences']['alert_frequency']}): ").strip()
                if frequency and frequency in ['immediate', 'daily', 'weekly']:
                    recipient['alert_preferences']['alert_frequency'] = frequency
                
                print(f"✅ Updated {recipient['name']}")
            except ValueError:
                print("❌ Invalid input, keeping current values")
        else:
            print("❌ Invalid choice")
    except ValueError:
        print("❌ Invalid input")
    
    return recipients

def configure_server(server_config):
    """Configure email server settings"""
    print("\n⚙️ Email Server Configuration")
    print("-" * 40)
    
    print("Current settings (press Enter to keep current):")
    smtp_server = input(f"SMTP Server (current: {server_config.get('smtp_server', 'smtp.gmail.com')}): ").strip()
    if smtp_server:
        server_config['smtp_server'] = smtp_server
    
    smtp_port = input(f"SMTP Port (current: {server_config.get('smtp_port', 587)}): ").strip()
    if smtp_port:
        try:
            server_config['smtp_port'] = int(smtp_port)
        except ValueError:
            print("❌ Invalid port number")
    
    sender_email = input(f"Sender Email (current: {server_config.get('sender_email', 'your_email@gmail.com')}): ").strip()
    if sender_email:
        server_config['sender_email'] = sender_email
    
    sender_password = input(f"Sender Password (current: {'*' * len(server_config.get('sender_password', ''))}): ").strip()
    if sender_password:
        server_config['sender_password'] = sender_password
    
    sender_name = input(f"Sender Name (current: {server_config.get('sender_name', 'Weee! Price Tracker')}): ").strip()
    if sender_name:
        server_config['sender_name'] = sender_name
    
    print("✅ Server configuration updated")
    return server_config

def test_email_system():
    """Test the email system"""
    print("\n🧪 Testing Email System")
    print("-" * 30)
    
    try:
        # Load current configuration
        recipients, server_config = load_email_config()
        
        if not recipients:
            print("❌ No recipients configured")
            return False
        
        # Check if email server is configured
        if not server_config.get('sender_email') or not server_config.get('sender_password'):
            print("❌ Email server not configured. Please configure server settings first.")
            return False
        
        # Test with first enabled recipient
        enabled_recipients = [r for r in recipients if r['enabled']]
        if not enabled_recipients:
            print("❌ No enabled recipients found")
            return False
        
        test_recipient = enabled_recipients[0]
        
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Create test message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{server_config['sender_name']} <{server_config['sender_email']}>"
        msg['To'] = test_recipient['email']
        msg['Subject'] = "Test Email - Weee! Price Tracker"
        
        text_body = f"""
Dear {test_recipient['name']},

This is a test email from your Weee! Price Tracker system.

If you receive this email, your email configuration is working correctly!

Best regards,
Your Weee! Price Tracker
        """
        
        msg.attach(MIMEText(text_body, 'plain'))
        
        # Send test email
        server = smtplib.SMTP(server_config['smtp_server'], server_config['smtp_port'])
        server.starttls()
        server.login(server_config['sender_email'], server_config['sender_password'])
        server.sendmail(server_config['sender_email'], test_recipient['email'], msg.as_string())
        server.quit()
        
        print(f"✅ Test email sent to {test_recipient['name']} ({test_recipient['email']})")
        return True
        
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        return False

def main():
    """Main email management interface"""
    print("📧 Weee! Price Tracker - Email Management")
    print("=" * 50)
    
    # Load current configuration
    recipients, server_config = load_email_config()
    
    while True:
        print("\n📋 Menu:")
        print("1. View recipients")
        print("2. Add recipient")
        print("3. Remove recipient")
        print("4. Toggle recipient (enable/disable)")
        print("5. Edit recipient preferences")
        print("6. Configure email server")
        print("7. Test email system")
        print("8. Save and exit")
        print("0. Exit without saving")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            show_recipients(recipients)
        elif choice == '2':
            recipients = add_recipient(recipients)
        elif choice == '3':
            recipients = remove_recipient(recipients)
        elif choice == '4':
            recipients = toggle_recipient(recipients)
        elif choice == '5':
            recipients = edit_recipient(recipients)
        elif choice == '6':
            server_config = configure_server(server_config)
        elif choice == '7':
            test_email_system()
        elif choice == '8':
            save_email_config(recipients, server_config)
            print("✅ Configuration saved!")
            break
        elif choice == '0':
            print("❌ Changes not saved")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main() 