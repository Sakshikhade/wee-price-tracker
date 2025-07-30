#!/usr/bin/env python3
# run_tracker.py - Easy launcher for the price tracker

import sys
import os

# Add the scripts directory to the path
script_dir = os.path.join(os.path.dirname(__file__), 'scripts')
sys.path.insert(0, script_dir)

def main():
    print("🛍️ Weee! Price Tracker")
    print("=" * 30)
    print("1. Run scraper once")
    print("2. Start daily scheduler")
    print("3. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                print("\n🚀 Running scraper once...")
                os.system(f'python3 "{os.path.join(script_dir, "scrape_wee.py")}"')
                break
            elif choice == '2':
                print("\n🤖 Starting daily scheduler...")
                print("The scraper will run every day at 9:00 AM")
                os.system(f'python3 "{os.path.join(script_dir, "scheduler.py")}"')
                break
            elif choice == '3':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
