#!/usr/bin/env python3
# scripts/setup_project.py - Complete project setup

import os
import sys
import subprocess
from pathlib import Path

def setup_python_path():
    """Add project root to Python path"""
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    print(f"✅ Added {project_root} to Python path")

def create_directories():
    """Create necessary directories"""
    directories = [
        "data/processed",
        "config",
        "logs",
        "venv"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")

def install_dependencies():
    """Install project dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_imports():
    """Test all imports"""
    print("�� Testing imports...")
    
    # Test environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ python-dotenv imported")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
    
    # Test email config
    try:
        from config.email_config import EMAIL_SERVER_CONFIG
        print("✅ Email config imported")
    except ImportError as e:
        print(f"❌ Email config import failed: {e}")
    
    # Test scraper
    try:
        from scripts.scrape_wee import TRACKED_PRODUCTS
        print("✅ Scraper imported")
    except ImportError as e:
        print(f"❌ Scraper import failed: {e}")

def main():
    """Main setup function"""
    print("🛍️ Weee! Price Tracker - Complete Setup")
    print("=" * 50)
    
    # Setup Python path
    setup_python_path()
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed. Please install dependencies manually.")
        return
    
    # Test imports
    test_imports()
    
    print("\n�� Setup complete!")
    print("\n📋 Next steps:")
    print("1. Activate virtual environment: source venv/bin/activate")
    print("2. Configure .env file with your settings")
    print("3. Run: python scripts/test_env.py")
    print("4. Start tracking: python run_tracker.py")

if __name__ == "__main__":
    main() 