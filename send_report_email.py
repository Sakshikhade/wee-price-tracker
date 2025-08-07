#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import sys

def send_report_email():
    try:
        from scripts.email_config import RECIPIENTS, EMAIL_SERVER_CONFIG
        
        # Get report file from command line argument
        if len(sys.argv) < 2:
            print("❌ No report file specified")
            return False
            
        report_file = sys.argv[1]
        if not os.path.exists(report_file):
            print(f"❌ Report file not found: {report_file}")
            return False
        
        # Read report content
        with open(report_file, 'r') as f:
            report_content = f.read()
        
        print(f"📄 Report content length: {len(report_content)} characters")
        
        # Send to all enabled recipients
        enabled_recipients = [r for r in RECIPIENTS if r['enabled']]
        
        if not enabled_recipients:
            print("❌ No enabled recipients found")
            return False
        
        print(f"📧 Sending to {len(enabled_recipients)} recipients...")
        
        for recipient in enabled_recipients:
            try:
                msg = MIMEMultipart('alternative')
                msg['From'] = f"{EMAIL_SERVER_CONFIG['sender_name']} <{EMAIL_SERVER_CONFIG['sender_email']}>"
                msg['To'] = recipient['email']
                msg['Subject'] = f"📊 Weee! Price Tracker - Daily Report ({datetime.now().strftime('%Y-%m-%d')})"
                
                # Create HTML version
                html_content = f"""
<html>
<body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
        <h2 style="color: #28a745;">🚀 Weee! Price Tracker - Daily Report</h2>
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Recipient:</strong> {recipient['name']}</p>
        
        <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <pre style="font-family: monospace; white-space: pre-wrap;">{report_content}</pre>
        </div>
        
        <p style="color: #666; font-size: 12px;">
            This is an automated report from your Weee! Price Tracker system.
        </p>
    </div>
</body>
</html>
                """
                
                msg.attach(MIMEText(report_content, 'plain'))
                msg.attach(MIMEText(html_content, 'html'))

                
                print(f"✅ Report sent to {recipient['name']} ({recipient['email']})")
                
            except Exception as e:
                print(f"❌ Failed to send to {recipient['name']}: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Email send failed: {e}")
        return False

if __name__ == "__main__":
    success = send_report_email()
    sys.exit(0 if success else 1)
