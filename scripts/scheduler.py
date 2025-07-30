# scripts/scheduler.py

import schedule
import time
import subprocess
import sys
import os
from datetime import datetime

def run_scraper():
    """Run the price tracker scraper"""
    try:
        print(f"\n{'='*50}")
        print(f"🕒 Running price tracker at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*50}")
        
        # Get the directory of this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        scraper_path = os.path.join(script_dir, 'scrape_wee.py')
        
        # Run the scraper
        result = subprocess.run([sys.executable, scraper_path], 
                              capture_output=True, text=True, cwd=script_dir)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("✅ Scraper completed successfully")
        else:
            print(f"❌ Scraper failed with return code {result.returncode}")
            
    except Exception as e:
        print(f"❌ Error running scraper: {e}")

def main():
    """Main scheduler function"""
    print("🤖 Price Tracker Scheduler Started")
    print("📅 Will run daily at 9:00 AM")
    print("🛑 Press Ctrl+C to stop")
    
    # Schedule the scraper to run daily at 9:00 AM
    schedule.every().day.at("09:00").do(run_scraper)
    
    # Also run once immediately for testing
    print("\n🧪 Running initial test...")
    run_scraper()
    
    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n👋 Scheduler stopped by user")

if __name__ == "__main__":
    main()
