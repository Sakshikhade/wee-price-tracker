# 📧 Multi-Recipient Email Alert System Setup Guide

## 🚀 Quick Start

### **Step 1: Set Up Email Alerts**
```bash
python3 scripts/setup_email_alerts.py
```
This will guide you through:
- Configuring your Gmail account
- Adding recipients
- Setting alert preferences

### **Step 2: Test the Configuration**
```bash
python3 scripts/setup_email_alerts.py test
```

### **Step 3: Run the Tracker**
```bash
python3 run_tracker.py
```

## 🔧 Advanced Email Management

### **Manage Recipients**
```bash
python3 scripts/manage_emails.py
```

This interactive tool allows you to:
- ✅ View all recipients
- ➕ Add new recipients
- ❌ Remove recipients
- 🔄 Enable/disable recipients
- ✏️ Edit recipient preferences
- ⚙️ Configure server settings
- 🧪 Test email system

## 📧 Email Alert Features

### **Multi-Recipient Support**
- Add unlimited recipients
- Individual preferences per recipient
- Enable/disable recipients easily
- Different alert thresholds per person

### **Smart Alert Management**
- **Spam Prevention**: Daily limits and cooldown periods
- **Individual Preferences**: Min savings, percentage, frequency
- **Alert History**: Tracks sent alerts to prevent duplicates
- **Flexible Scheduling**: Immediate, daily, or weekly alerts

### **Beautiful Email Templates**
- **HTML Formatting**: Rich, professional-looking emails
- **Product Links**: Direct links to products
- **Savings Calculation**: Shows amount and percentage saved
- **Responsive Design**: Works on all email clients

## 🛠️ Configuration Options

### **Per-Recipient Settings**
```python
{
    'email': 'recipient@gmail.com',
    'name': 'John Doe',
    'enabled': True,
    'alert_preferences': {
        'minimum_savings': 1.00,      # Minimum $ savings
        'minimum_percentage': 5.0,    # Minimum % drop
        'alert_frequency': 'immediate' # immediate/daily/weekly
    }
}
```

### **Global Settings**
```python
GLOBAL_ALERT_SETTINGS = {
    'enable_alerts': True,
    'include_product_link': True,
    'email_subject_prefix': '🚨 Weee! Price Drop Alert: ',
    'max_alerts_per_day': 5,          # Prevent spam
    'alert_cooldown_hours': 6         # Hours between alerts
}
```

## 📋 Usage Examples

### **Add a New Recipient**
```bash
python3 scripts/manage_emails.py
# Choose option 2: "Add recipient"
# Enter name, email, and preferences
```

### **Test Email System**
```bash
python3 scripts/manage_emails.py
# Choose option 7: "Test email system"
```

### **Edit Recipient Preferences**
```bash
python3 scripts/manage_emails.py
# Choose option 5: "Edit recipient preferences"
```

## 🔐 Gmail Setup

### **1. Enable 2-Step Verification**
1. Go to your Google Account settings
2. Enable 2-Step Verification

### **2. Generate App Password**
1. Go to Security → App passwords
2. Generate new app password for "Mail"
3. Use the 16-character password (not your regular password)

### **3. Configure Email Settings**
```bash
python3 scripts/setup_email_alerts.py
# Enter your Gmail and app password
```

## 📊 Alert Examples

### **Console Alert**
```
🚨 PRICE DROP ALERT!
Product: Maggi Masala Instant Noodles 9.8 oz
Old Price: $4.99
New Price: $3.99
Savings: $1.00 (20.0% off)
--------------------------------------------------
✅ Email sent to John Doe (john@gmail.com)
📧 Sent 1 email alert(s)
```

### **Email Alert**
- **Subject**: 🚨 Weee! Price Drop Alert: Maggi Masala Instant Noodles 9.8 oz
- **Content**: Beautiful HTML email with product details and savings
- **Action Button**: Direct link to the product

## 🚨 Troubleshooting

### **Email Not Sending**
1. Check Gmail app password is correct
2. Verify 2-Step Verification is enabled
3. Test SMTP connection: `python3 scripts/setup_email_alerts.py test`

### **No Alerts Received**
1. Check recipient is enabled
2. Verify alert preferences (min savings/percentage)
3. Check spam folder
4. Review alert history for cooldown periods

### **Too Many Alerts**
1. Adjust `max_alerts_per_day` in global settings
2. Increase `alert_cooldown_hours`
3. Set higher minimum savings/percentage thresholds

## 📁 File Structure

```
wee-price-tracker/
├── config/
│   └── email_config.py          # Email configuration
├── scripts/
│   ├── scrape_wee.py           # Updated with multi-recipient support
│   ├── manage_emails.py        # Email management tool
│   └── setup_email_alerts.py   # Quick setup script
└── data/processed/
    └── alert_history.json      # Alert tracking (auto-created)
```

## 🎯 Key Benefits

1. **Easy Management**: No need to edit code files
2. **Multiple Recipients**: Alert different people with different preferences
3. **Smart Alerts**: Prevent spam with intelligent limits
4. **Beautiful Emails**: Professional HTML formatting
5. **Flexible Configuration**: Per-recipient and global settings
6. **Testing Tools**: Built-in testing and validation

## 🚀 Next Steps

1. **Set up email alerts**: `python3 scripts/setup_email_alerts.py`
2. **Add recipients**: Use the management tool
3. **Test the system**: Run a test scrape
4. **Monitor alerts**: Check email and console output
5. **Customize preferences**: Adjust thresholds as needed

Your multi-recipient email alert system is now ready to notify multiple people about price drops with beautiful, professional emails! 🎉 