# 🛍️ Weee! Price Tracker

An intelligent price tracking system that monitors specific products on Weee! and sends alerts when prices drop.

## ✨ Features

- 🎯 **Targeted Tracking**: Monitor specific products you care about
- 📉 **Price Drop Alerts**: Get notified when prices decrease
- 📊 **Historical Data**: Track price changes over time
- 🤖 **Automated Scheduling**: Run daily checks automatically
- 📧 **Email Notifications**: Optional email alerts for price drops
- 🔍 **Smart Matching**: Fuzzy matching to find products even with slight name variations

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Tracked Products
Edit the `TRACKED_PRODUCTS` list in `scripts/scrape_wee.py`:
```python
TRACKED_PRODUCTS = [
    "Maggi Masala Instant Noodles 9.8 oz",
    "Lee Kum Kee Supreme Soy Sauce 500 ml",
    # Add your products here
]
```

### 3. Run the Tracker
```bash
# Run once
python3 run_tracker.py

# Or run the scraper directly
python3 scripts/scrape_wee.py

# Or start the daily scheduler
python3 scripts/scheduler.py
```

## 📧 Email Alerts Setup (Optional)

### 1. Configure Email Settings
1. Copy `config/email_config.py` to create your personal config
2. Edit the email settings:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your_email@gmail.com',
    'sender_password': 'your_app_password',  # Use Gmail app password
    'recipient_email': 'your_email@gmail.com',
}
```

### 2. Enable Email Alerts
Uncomment the email configuration import in `scripts/scrape_wee.py`:
```python
# Uncomment these lines to enable email alerts
# try:
#     from config.email_config import EMAIL_CONFIG
# except ImportError:
#     EMAIL_CONFIG = None
```

### 3. Gmail Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an app password: [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
3. Use the app password (not your regular password) in the config

## 📁 Project Structure

```
wee-price-tracker/
├── README.md
├── requirements.txt
├── run_tracker.py          # Easy launcher script
├── config/
│   └── email_config.py     # Email configuration template
├── data/
│   └── processed/
│       ├── wee_prices.csv      # Scraped product data
│       └── price_history.json  # Price tracking history
├── scripts/
│   ├── scrape_wee.py       # Main scraper with price tracking
│   ├── scheduler.py        # Daily automation scheduler
│   └── analyze_data.py     # Data analysis script
└── notebooks/
    └── visualize_data.ipynb # Data visualization notebook
```

## 🔧 How It Works

### 1. Product Tracking
- The scraper searches for your specified products on Weee!
- Uses fuzzy matching to find products even with slight name variations
- Only tracks products in your `TRACKED_PRODUCTS` list

### 2. Price Comparison
- Stores historical price data in `data/processed/price_history.json`
- Compares current prices with previous prices
- Detects price drops and calculates savings

### 3. Alert System
- **Console Alerts**: Always shows price drops in the terminal
- **Email Alerts**: Optional email notifications (requires configuration)
- Shows old price, new price, and savings amount/percentage

### 4. Scheduling
- Run `scheduler.py` to check prices daily at 9:00 AM
- Runs continuously in the background
- Logs all activity with timestamps

## 📊 Data Output

### CSV Data (`data/processed/wee_prices.csv`)
- Product Name, Price, Unit, Brand, Category
- Timestamp of each scrape
- Source selector used for extraction

### Price History (`data/processed/price_history.json`)
```json
{
  "Product Name": {
    "price": 5.99,
    "timestamp": "2025-07-27T10:30:00",
    "price_str": "$5.99"
  }
}
```

## 🛠️ Customization

### Add More Products
Edit the `TRACKED_PRODUCTS` list in `scripts/scrape_wee.py`:
```python
TRACKED_PRODUCTS = [
    "Your Product Name Here",
    "Another Product",
    # Add as many as you want
]
```

### Change Schedule
Edit `scripts/scheduler.py` to change when the scraper runs:
```python
# Run daily at 9:00 AM
schedule.every().day.at("09:00").do(run_scraper)

# Other options:
# schedule.every(6).hours.do(run_scraper)  # Every 6 hours
# schedule.every().monday.at("10:00").do(run_scraper)  # Weekly
```

### Modify Alert Threshold
You can add a minimum savings threshold before sending alerts:
```python
# In the check_price_drops function
if last_price and current_price < last_price:
    savings = last_price - current_price
    if savings >= 1.00:  # Only alert for $1+ savings
        send_price_alert(name, last_price, current_price)
```

## 🚨 Troubleshooting

### No Products Found
- Check if the products are available on the sale page
- Try searching different category pages
- Products might be out of stock
- Website structure might have changed

### Email Alerts Not Working
- Verify your Gmail app password is correct
- Check that 2-factor authentication is enabled
- Ensure email config file is properly imported
- Check spam folder for alert emails

### Scheduler Issues
- Make sure the schedule library is installed: `pip install schedule`
- Check that the script has the correct file paths
- Run once manually first to ensure the scraper works

## 📈 Future Enhancements

- [ ] Support for multiple websites
- [ ] Web dashboard for price tracking
- [ ] Mobile push notifications
- [ ] Price prediction using machine learning
- [ ] Multiple alert thresholds
- [ ] Webhook support for other notification services

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the price tracker!

## ⚠️ Disclaimer

This tool is for personal use only. Please respect website terms of service and don't overload servers with too frequent requests. Use responsibly and ethically.
