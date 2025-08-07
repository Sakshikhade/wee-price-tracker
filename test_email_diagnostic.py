#!/usr/bin/env python3
# Email Diagnostic Script

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sys
import os

def test_email_connection():
    """Test SMTP connection and authentication"""
    print("🔍 Testing Email Connection...")
    
    try:
        from scripts.email_config import EMAIL_SERVER_CONFIG, RECIPIENTS
        
        print(f"📧 Server: {EMAIL_SERVER_CONFIG['smtp_server']}:{EMAIL_SERVER_CONFIG['smtp_port']}")
        print(f"📧 Sender: {EMAIL_SERVER_CONFIG['sender_email']}")
        print(f"📧 Recipients: {len(RECIPIENTS)}")
        
        # Test SMTP connection
        print("\n🔗 Testing SMTP connection...")
        server = smtplib.SMTP(EMAIL_SERVER_CONFIG['smtp_server'], EMAIL_SERVER_CONFIG['smtp_port'])
        server.starttls()
        print("✅ TLS started successfully")
        
        # Test login
        print("🔐 Testing authentication...")
        server.login(EMAIL_SERVER_CONFIG['sender_email'], EMAIL_SERVER_CONFIG['sender_password'])
        print("✅ Authentication successful")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        print("💡 This usually means:")
        print("   - Wrong password")
        print("   - Need to use App Password instead of regular password")
        print("   - 2-Factor Authentication not enabled")
        return False
        
    except smtplib.SMTPConnectError as e:
        print(f"❌ Connection failed: {e}")
        print("💡 Check your internet connection")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_email_send():
    """Test sending a simple email"""
    print("\n📤 Testing Email Send...")
    
    try:
        from scripts.email_config import EMAIL_SERVER_CONFIG, RECIPIENTS
        
        # Get first enabled recipient
        enabled_recipients = [r for r in RECIPIENTS if r['enabled']]
        if not enabled_recipients:
            print("❌ No enabled recipients found")
            return False
            
        test_recipient = enabled_recipients[0]
        print(f"📧 Testing with: {test_recipient['name']} ({test_recipient['email']})")
        
        # Create test message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{EMAIL_SERVER_CONFIG['sender_name']} <{EMAIL_SERVER_CONFIG['sender_email']}>"
        msg['To'] = test_recipient['email']
        msg['Subject'] = f"🧪 Email Test - Weee! Price Tracker ({datetime.now().strftime('%Y-%m-%d %H:%M')})"
        
        text_body = f"""
Dear {test_recipient['name']},

This is a test email from your Weee! Price Tracker system.

If you receive this email, your email configuration is working correctly!

Test Details:
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Sender: {EMAIL_SERVER_CONFIG['sender_email']}
- Recipient: {test_recipient['email']}

Best regards,
Your Weee! Price Tracker
        """
        
        html_body = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
        <h2 style="color: #28a745;">🧪 Email Test - Weee! Price Tracker</h2>
        <p>Dear {test_recipient['name']},</p>
        <p>This is a test email from your Weee! Price Tracker system.</p>
        
        <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <p><strong>If you receive this email, your email configuration is working correctly!</strong></p>
            <p><strong>Test Details:</strong></p>
            <ul>
                <li>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</li>
                <li>Sender: {EMAIL_SERVER_CONFIG['sender_email']}</li>
                <li>Recipient: {test_recipient['email']}</li>
            </ul>
        </div>
        
        <p>Best regards,<br>Your Weee! Price Tracker</p>
    </div>
</body>
</html>
        """
        
        msg.attach(MIMEText(text_body, 'plain'))
        msg.attach(MIMEText(html_body, 'html'))
        
        # Send email
        print("📤 Sending test email...")
        server = smtplib.SMTP(EMAIL_SERVER_CONFIG['smtp_server'], EMAIL_SERVER_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_SERVER_CONFIG['sender_email'], EMAIL_SERVER_CONFIG['sender_password'])
        server.sendmail(EMAIL_SERVER_CONFIG['sender_email'], test_recipient['email'], msg.as_string())
        server.quit()
        
        print(f"✅ Test email sent successfully to {test_recipient['email']}")
        print("📧 Please check your email (including spam folder)")
        return True
        
    except Exception as e:
        print(f"❌ Email send failed: {e}")
        return False

def check_spam_filters():
    """Provide tips about spam filters"""
    print("\n📋 Spam Filter Tips:")
    print("1. Check your spam/junk folder")
    print("2. Add the sender email to your contacts")
    print("3. Mark the email as 'Not Spam' if found in spam")
    print("4. Check your email provider's spam settings")

def main():
    print("🔍 Weee! Price Tracker - Email Diagnostic")
    print("=" * 50)
    
    # Test 1: Connection
    if test_email_connection():
        print("\n✅ SMTP connection and authentication successful")
        
        # Test 2: Send email
        if test_email_send():
            print("\n✅ Email sent successfully!")
            check_spam_filters()
        else:
            print("\n❌ Email sending failed")
    else:
        print("\n❌ Email connection failed")
        print("\n💡 Troubleshooting steps:")
        print("1. Verify your Gmail App Password is correct")
        print("2. Make sure 2-Factor Authentication is enabled")
        print("3. Check your internet connection")
        print("4. Try generating a new App Password")

if __name__ == "__main__":
    main() 