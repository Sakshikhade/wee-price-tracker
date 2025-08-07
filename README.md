# 🛍️ Weee! Price Tracker

An intelligent price tracking system that monitors Indian grocery products on Weee! and sends alerts when prices drop. Perfect for tracking your favorite Indian groceries and getting the best deals!

![Weee! Price Tracker Screenshot](Screenshot%202025-08-07%20at%203.54.17%20PM.png)

## ✨ Features

- 🎯 **Comprehensive Indian Grocery Tracking**: Monitor 58+ Indian grocery products
- 📉 **Smart Price Drop Alerts**: Get notified when prices decrease with detailed savings info
- 📊 **Historical Data Tracking**: Track price changes over time with CSV and JSON storage
- 🤖 **Automated Scheduling**: Run daily checks automatically with customizable timing
- 📧 **Multi-Recipient Email Notifications**: Send alerts to multiple people with personalized settings
- 🔍 **Advanced Fuzzy Matching**: Find products even with slight name variations
- 🚀 **Complete System Runner**: One-command execution with virtual environment management
- 📋 **Comprehensive Reports**: Generate detailed daily reports with system status
- 🔧 **Easy Configuration**: Simple .env file setup for all settings

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd wee-price-tracker
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file with your settings:
```ini
# Email Configuration
EMAIL_SENDER_ADDRESS=your_email@gmail.com
EMAIL_SENDER_PASSWORD=your_gmail_app_password
EMAIL_SENDER_NAME=Weee! Price Tracker

# Product Tracking (58+ Indian grocery items)
TRACKED_PRODUCTS=["Indian Eggplant 2 lb", "Indian Bitter Melon 2 lb", "Indian okra 0.9-1.1 lb", "Red onions 2 lb bag", "Roma tomatoes 2 lb bag", "Fresh ginger 0.95-1.05 lb", "Green onion 1 bunch", "Cauliflower 1 head", "Spinach 1 bunch", "Sleeved garlic pack 5 ct", "Green cabbage 1 head", "Yellow onion 3 lb bag", "Persian cucumbers 0.9-1.1 lb", "Idaho russet potatoes 5 lb", "Green bell pepper", "Opo squash 1 pc", "Green beans 0.9-1.1 lb", "Carrots 2 lb bag", "Cilantro 1 bunch", "Curry leaves 0.25 oz", "Mint 1 bunch", "Bananas 2.6-3 lb", "Mini spicy green chilies 226 g bag", "Maggi Masala instant noodles 9.8 oz", "Deep Paneer Paratha Frozen 4 pcs 13 oz", "Deep Bhagwati's Methi Thepla 9 oz", "Deep ClayOven Tandoori Naan Family Pack 42.4 oz", "Deep Family Pack Homestyle Paratha 20 pcs 46 oz", "Franco uncooked phulka 18 pcs 1.31 lb", "Laxmi Poha Flattened Rice Thick 4 lb", "Shastha Dosa Batter 32 oz", "India Gate Basmati Rice", "Laxmi Idli Rice 20 lb", "Regal Sona Masoori Rice 20 lb", "Laxmi Ponni Boiled Rice 20 lb", "Aashirvaad Whole Wheat Atta Flour 20 lb", "Laxmi Besan gram flour 2 lb", "Laxmi Toor Dal Split Pigeon Peas 4 lb", "Laxmi Moong Dal Skinned mung beans 4 lb", "Laxmi Yellow Split Peas 4 lb", "Laxmi Urad Dal Split 4 lb", "Laxmi Chana Dal 4 lb", "Laxmi Kabuli Chana chickpeas 4 lb", "Laxmi Kala Chana black chickpeas 4 lb", "Laxmi Urad Gota black whole lentil 4 lb", "Laxmi Urad Dal skinned 4 lb", "Laxmi Sabudana tapioca 4 lb", "Vadilal Paneer Block", "Nanak Plain Paneer 400 g", "Pavel's whole-milk yogurt 32 oz", "Amul Ghee clarified butter", "Garvi Gujarat Gujarati Chakri 10 oz", "Kurkure Masala Munch chips", "Kurkure Chilli Chatka chips", "Lay's Magic Masala chips 1.82 oz", "Laxmi Puffed Rice 14 oz", "Ching's Schezwan chutney", "Lee Kum Kee Supreme Soy Sauce 500 ml", "Aara Cumin Seeds", "TSF Barramundi Whole Cleaned 500-550 g"]
```

### 3. Run the Complete System
```bash
# Make the script executable
chmod +x run_complete_tracker.sh

# Run the complete system (scraper + analysis + email report)
./run_complete_tracker.sh
```

## 📧 Email Alerts Setup

### 1. Configure Email Recipients
```bash
python3 scripts/manage_emails.py
```
This interactive tool helps you:
- Add multiple recipients with personalized settings
- Configure email server settings
- Set minimum savings thresholds
- Test email delivery

### 2. Gmail App Password Setup
1. Enable 2-factor authentication on your Gmail account
2. Generate an app password: [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
3. Use the app password in your `.env` file

### 3. Email Features
- **Multi-Recipient Support**: Send alerts to multiple people
- **Personalized Settings**: Different thresholds for each recipient
- **HTML Email Templates**: Beautiful, formatted email alerts
- **Spam Prevention**: Cooldown periods and daily limits
- **Detailed Reports**: Comprehensive daily system reports

## 📁 Project Structure

```
wee-price-tracker/
├── README.md
├── requirements.txt
├── run_complete_tracker.sh    # 🚀 Complete system runner
├── run_tracker.py             # Simple launcher script
├── .env                       # Environment configuration
├── config/
│   └── email_config.py        # Email configuration
├── data/
│   └── processed/
│       ├── wee_prices.csv     # Scraped product data
│       └── price_history.json # Price tracking history
├── scripts/
│   ├── scrape_wee.py          # Main scraper with advanced matching
│   ├── manage_emails.py       # Email configuration tool
│   ├── email_config.py        # Email settings and templates
│   ├── scheduler.py           # Daily automation scheduler
│   └── analyze_data.py        # Data analysis script
├── reports/                   # Generated daily reports
├── logs/                      # Execution logs
└── notebooks/
    └── visualize_data.ipynb   # Data visualization notebook
```

## 🛍️ Tracked Products

The system tracks **58+ Indian grocery products** across these categories:

### 🥬 Fresh Vegetables (18 items)
- Indian Eggplant, Bitter Melon, Okra, Onions, Tomatoes, Ginger, Green Onion, Cauliflower, Spinach, Garlic, Cabbage, Cucumbers, Potatoes, Bell Pepper, Squash, Green Beans, Carrots

### 🌿 Fresh Herbs (3 items)
- Cilantro, Curry Leaves, Mint

### 🍌 Fresh Fruits (1 item)
- Bananas

### 🌶️ Fresh Chilies (1 item)
- Mini Spicy Green Chilies

### 🍜 Instant Noodles (1 item)
- Maggi Masala Noodles

### ❄️ Frozen Items (5 items)
- Deep Paneer Paratha, Methi Thepla, Tandoori Naan, Homestyle Paratha, Franco Phulka

### 🍚 Rice Products (6 items)
- Laxmi Poha, Shastha Dosa Batter, India Gate Basmati, Laxmi Idli Rice, Regal Sona Masoori, Laxmi Ponni Rice

### 🍞 Flour Products (2 items)
- Aashirvaad Atta Flour, Laxmi Besan

### 🫘 Pulses/Lentils (10 items)
- Various Laxmi Dal products (Toor, Moong, Yellow Split Peas, Urad, Chana, Kabuli Chana, Kala Chana, Urad Gota, Sabudana)

### 🥛 Dairy Products (4 items)
- Vadilal Paneer, Nanak Paneer, Pavel's Yogurt, Amul Ghee

### 🍿 Snacks (4 items)
- Garvi Gujarat Chakri, Kurkure Chips (2 types), Lay's Magic Masala

### 🍚 Rice/Snack Base (1 item)
- Laxmi Puffed Rice

### 🥄 Condiments/Sauces (2 items)
- Ching's Schezwan Chutney, Lee Kum Kee Soy Sauce

### 🌶️ Spices (1 item)
- Aara Cumin Seeds

### 🐟 Fish (1 item)
- TSF Barramundi

## 🔧 How It Works

### 1. Advanced Product Matching
- Uses fuzzy string matching with 60% similarity threshold
- Brand-specific keyword matching (Laxmi, Deep, Aashirvaad, etc.)
- Product type matching (rice, dal, paneer, etc.)
- Handles slight name variations and different formats

### 2. Smart Price Tracking
- Stores historical price data in JSON format
- Compares current prices with previous prices
- Calculates savings amount and percentage
- Prevents duplicate alerts with cooldown periods

### 3. Multi-Channel Alerts
- **Console Alerts**: Real-time price drop notifications
- **Email Alerts**: HTML-formatted emails with detailed savings info
- **Daily Reports**: Comprehensive system status reports
- **Logging**: Detailed execution logs for debugging

### 4. Automated Scheduling
- Daily price checks at configurable times
- Background execution with proper error handling
- Automatic retry on failures
- System status monitoring

## 📊 Data Output

### CSV Data (`data/processed/wee_prices.csv`)
```csv
Product Name,Price,Unit,Brand,Category,Timestamp,Source
TSF Barramundi Whole Cleaned 500-550 g,$5.88,,TSF,Fish,2025-08-07T15:29:12,div[data-testid*="product"]
```

### Price History (`data/processed/price_history.json`)
```json
{
  "TSF Barramundi Whole Cleaned 500-550 g": {
    "price": 5.88,
    "timestamp": "2025-08-07T15:29:12",
    "price_str": "$5.88"
  }
}
```

### Daily Reports (`reports/daily_report_YYYYMMDD_HHMMSS.txt`)
- Scraper results summary
- Data analysis statistics
- System status information
- Email configuration status
- Tracked products list

## 🚀 Usage Examples

### Run Once
```bash
# Simple run
python3 scripts/scrape_wee.py

# Complete system with email report
./run_complete_tracker.sh
```

### Schedule Daily Runs
```bash
# Start the scheduler
python3 scripts/scheduler.py

# Or use cron (Linux/Mac)
0 9 * * * cd /path/to/wee-price-tracker && ./run_complete_tracker.sh
```

### Email Management
```bash
# Configure email settings
python3 scripts/manage_emails.py

# Test email delivery
python3 test_email_diagnostic.py
```

## 🛠️ Customization

### Add More Products
Edit the `TRACKED_PRODUCTS` list in your `.env` file:
```ini
TRACKED_PRODUCTS=["Your Product Name", "Another Product", ...]
```

### Modify Alert Thresholds
In `scripts/email_config.py`:
```python
'alert_preferences': {
    'minimum_savings': 1.00,      # Minimum $1 savings
    'minimum_percentage': 5.0,     # Minimum 5% discount
    'alert_frequency': 'immediate' # 'immediate', 'daily', 'weekly'
}
```

### Change Schedule
Edit `scripts/scheduler.py`:
```python
# Run daily at 9:00 AM
schedule.every().day.at("09:00").do(run_scraper)

# Other options:
# schedule.every(6).hours.do(run_scraper)     # Every 6 hours
# schedule.every().monday.at("10:00").do(run_scraper)  # Weekly
```

## 🚨 Troubleshooting

### No Products Found
- Check if products are available on the sale page
- Verify product names match exactly
- Enable debug mode: `DEBUG_MODE=true` in `.env`
- Check website structure changes

### Email Alerts Not Working
- Verify Gmail app password is correct
- Check 2-factor authentication is enabled
- Test email delivery: `python3 test_email_diagnostic.py`
- Check spam folder for alert emails
- Verify email configuration: `python3 scripts/manage_emails.py`

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Permission Issues
```bash
# Make scripts executable
chmod +x run_complete_tracker.sh
chmod +x scripts/*.py
```

## 📈 Future Enhancements

- [ ] Web dashboard for price tracking visualization
- [ ] Mobile push notifications
- [ ] Price prediction using machine learning
- [ ] Support for multiple grocery websites
- [ ] Integration with shopping list apps
- [ ] Price comparison across different stores
- [ ] Recipe-based product recommendations
- [ ] Seasonal price trend analysis

## 🤝 Contributing

We welcome contributions! Please feel free to:
- Submit issues and feature requests
- Create pull requests for improvements
- Add more Indian grocery products to track
- Improve the matching algorithms
- Enhance the email templates

## ⚠️ Disclaimer

This tool is for personal use only. Please:
- Respect website terms of service
- Don't overload servers with too frequent requests
- Use responsibly and ethically
- Consider the impact on the target website

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the logs in the `logs/` directory
3. Test individual components separately
4. Enable debug mode for detailed output

---

**Happy Price Tracking! 🛍️💰**
