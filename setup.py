#!/usr/bin/env python3
# setup.py - Setup script for the Weee! Price Tracker

import os
import subprocess
import sys

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = [
        "data/processed",
        "config"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created: {directory}")

def show_next_steps():
    """Show user what to do next"""
    print("\n🎉 Setup complete! Here's what to do next:")
    print("\n1. 📝 Configure tracked products:")
    print("   Edit the TRACKED_PRODUCTS list in scripts/scrape_wee.py")
    print("\n2. 🚀 Run the tracker:")
    print("   python3 run_tracker.py")
    print("\n3. 📧 (Optional) Set up email alerts:")
    print("   - Copy config/email_config.py and fill in your email details")
    print("   - Uncomment email import lines in scripts/scrape_wee.py")
    print("\n4. 🤖 (Optional) Set up daily automation:")
    print("   python3 scripts/scheduler.py")
    print("\n📚 For more information, check the README.md file!")

def main():
    """Main setup function"""
    print("🛍️ Weee! Price Tracker Setup")
    print("=" * 30)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed. Please install requirements manually.")
        return
    
    # Create directories
    create_directories()
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
