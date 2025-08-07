# 🔐 Environment Variables Setup Guide

## 📋 Overview

The Weee! Price Tracker now uses environment variables for secure configuration management. This allows you to:

- 🔒 **Secure Credentials**: Keep sensitive data out of code files
- ⚙️ **Easy Configuration**: Change settings without editing code
- 🚀 **Flexible Deployment**: Different settings for different environments
- 🔄 **Version Control Safe**: Sensitive data stays out of Git

## 🚀 Quick Setup

### **Step 1: Install Dependencies**
```bash
pip3 install python-dotenv
```

### **Step 2: Create Your .env File**
```bash
# Copy the template
cp .env.template .env

# Edit with your actual values
nano .env
```

### **Step 3: Configure Your Settings**
Edit the `.env` file with your actual values:

```bash
# Email Server Configuration
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER_ADDRESS=your_actual_email@gmail.com
EMAIL_SENDER_PASSWORD=your_actual_app_password
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
```

### **Step 4: Validate Configuration**
```bash
python3 scripts/env_loader.py validate
```

## 🔧 Environment Variables Reference

### **Email Configuration**
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `EMAIL_SMTP_SERVER` | SMTP server address | `smtp.gmail.com` | ✅ |
| `EMAIL_SMTP_PORT` | SMTP server port | `587` | ✅ |
| `EMAIL_SENDER_ADDRESS` | Your Gmail address | - | ✅ |
| `EMAIL_SENDER_PASSWORD` | Gmail app password | - | ✅ |
| `EMAIL_SENDER_NAME` | Sender display name | `Weee! Price Tracker` | ❌ |

### **Alert Settings**
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `EMAIL_ENABLE_ALERTS` | Enable email alerts | `true` | ❌ |
| `EMAIL_MAX_ALERTS_PER_DAY` | Max alerts per day | `5` | ❌ |
| `EMAIL_ALERT_COOLDOWN_HOURS` | Hours between alerts | `6` | ❌ |
| `EMAIL_SUBJECT_PREFIX` | Email subject prefix | `🚨 Weee! Price Drop Alert: ` | ❌ |

### **Product Tracking**
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `TRACKED_PRODUCTS` | JSON array of product names | `["Maggi...", "Lee Kum..."]` | ❌ |

### **Web Scraping**
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BASE_URL` | Weee! sale page URL | `https://www.sayweee.com/en/category/sale` | ❌ |
| `REQUEST_TIMEOUT` | Request timeout (seconds) | `10` | ❌ |
| `MAX_RETRIES` | Max retry attempts | `3` | ❌ |

### **Data Storage**
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATA_DIR` | Data directory | `data/processed` | ❌ |
| `PRICE_HISTORY_FILE` | Price history file | `price_history.json` | ❌ |
| `ALERT_HISTORY_FILE` | Alert history file | `alert_history.json` | ❌ |
| `CSV_OUTPUT_FILE` | CSV output file | `wee_prices.csv` | ❌ |

### **Logging**
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LOG_LEVEL` | Logging level | `INFO` | ❌ |
| `LOG_FILE` | Log file path | `logs/price_tracker.log` | ❌ |

### **Scheduler**
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SCHEDULER_RUN_TIME` | Daily run time | `09:00` | ❌ |
| `SCHEDULER_ENABLED` | Enable scheduler | `true` | ❌ |

### **Development**
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEBUG_MODE` | Enable debug mode | `false` | ❌ |
| `TEST_MODE` | Enable test mode | `false` | ❌ |

## 🔐 Security Best Practices

### **1. Never Commit .env Files**
The `.env` file is already in `.gitignore` to prevent accidental commits.

### **2. Use Gmail App Passwords**
- Enable 2-Step Verification on your Gmail account
- Generate an app password for "Mail"
- Use the 16-character app password (not your regular password)

### **3. Environment-Specific Files**
```bash
# Development
.env.development

# Production
.env.production

# Testing
.env.test
```

### **4. Template Files**
```bash
# Create template
cp .env.template .env.example

# Share template (safe to commit)
git add .env.example
```

## 🛠️ Management Commands

### **Validate Configuration**
```bash
python3 scripts/env_loader.py validate
```

### **Create Template**
```bash
python3 scripts/env_loader.py template
```

### **Load Configuration**
```bash
python3 scripts/env_loader.py load
```

## 📝 Example Configurations

### **Basic Setup**
```bash
# .env
EMAIL_SENDER_ADDRESS=your_email@gmail.com
EMAIL_SENDER_PASSWORD=abcd efgh ijkl mnop
TRACKED_PRODUCTS=["Product 1", "Product 2"]
```

### **Advanced Setup**
```bash
# .env
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER_ADDRESS=your_email@gmail.com
EMAIL_SENDER_PASSWORD=your_app_password
EMAIL_SENDER_NAME=Weee! Price Tracker

EMAIL_ENABLE_ALERTS=true
EMAIL_MAX_ALERTS_PER_DAY=3
EMAIL_ALERT_COOLDOWN_HOURS=12
EMAIL_SUBJECT_PREFIX=🚨 Price Drop: 

TRACKED_PRODUCTS=["Maggi Masala Instant Noodles 9.8 oz", "Lee Kum Kee Supreme Soy Sauce 500 ml"]

BASE_URL=https://www.sayweee.com/en/category/sale
REQUEST_TIMEOUT=15
MAX_RETRIES=5

DATA_DIR=data/processed
PRICE_HISTORY_FILE=price_history.json
ALERT_HISTORY_FILE=alert_history.json
CSV_OUTPUT_FILE=wee_prices.csv

LOG_LEVEL=DEBUG
LOG_FILE=logs/price_tracker.log

SCHEDULER_RUN_TIME=09:00
SCHEDULER_ENABLED=true

DEBUG_MODE=false
TEST_MODE=false
```

## 🔄 Updating Configuration

### **Add New Products**
```bash
# Edit .env file
TRACKED_PRODUCTS=["Product 1", "Product 2", "New Product 3"]
```

### **Change Alert Settings**
```bash
# Edit .env file
EMAIL_MAX_ALERTS_PER_DAY=10
EMAIL_ALERT_COOLDOWN_HOURS=2
```

### **Switch Environments**
```bash
# Development
cp .env.development .env

# Production
cp .env.production .env
```

## 🚨 Troubleshooting

### **Environment Variables Not Loading**
1. Check `.env` file exists in project root
2. Verify `python-dotenv` is installed
3. Ensure `load_dotenv()` is called in your script

### **Email Configuration Issues**
1. Verify Gmail app password is correct
2. Check 2-Step Verification is enabled
3. Test SMTP connection manually

### **Product Tracking Issues**
1. Validate JSON format in `TRACKED_PRODUCTS`
2. Check product names match exactly
3. Verify `BASE_URL` is accessible

### **Permission Issues**
1. Ensure `.env` file is readable
2. Check file permissions: `chmod 600 .env`
3. Verify user has access to data directories

## 📊 Monitoring

### **Check Current Configuration**
```bash
python3 scripts/env_loader.py validate
```

### **View Environment Variables**
```bash
# In Python
import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv('EMAIL_SENDER_ADDRESS'))
```

### **Debug Mode**
```bash
# Set in .env
DEBUG_MODE=true
```

## 🎯 Benefits

1. **Security**: Sensitive data stays out of code
2. **Flexibility**: Easy to change settings
3. **Deployment**: Different configs for different environments
4. **Collaboration**: Safe to share code without exposing secrets
5. **Maintenance**: Centralized configuration management

Your environment variables are now securely configured and ready to use! 🎉 