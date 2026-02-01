# Revenue Auto-Poster - Executes scheduled posts
# Run this script and it will automatically post at the right times

import json
import time
import requests
from datetime import datetime
import os

class AutoPoster:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.moltbook.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def publish_post(self, post_file):
        """Publish a post from JSON file"""
        with open(post_file, 'r', encoding='utf-8') as f:
            post_data = json.load(f)
        
        try:
            response = requests.post(
                f"{self.base_url}/posts",
                headers=self.headers,
                json=post_data
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_scheduler(self):
        """Execute posts according to schedule"""
        # Load schedule
        with open('post_schedule.json', 'r', encoding='utf-8') as f:
            schedule = json.load(f)
        
        print("🤖 REVENUE AUTO-POSTER ACTIVATED")
        print("=" * 70)
        print(f"Starting: {datetime.now().strftime('%H:%M:%S')}")
        print(f"Posts scheduled: {len(schedule)}")
        print()
        
        # Get post files
        post_files = sorted([f for f in os.listdir('.') if f.startswith('monetization_post_')])
        
        for i, (scheduled_item, post_file) in enumerate(zip(schedule, post_files), 1):
            scheduled_time = datetime.fromisoformat(scheduled_item['time'])
            now = datetime.now()
            
            # Calculate wait time
            wait_seconds = (scheduled_time - now).total_seconds()
            
            if wait_seconds > 0:
                print(f"⏳ Waiting {int(wait_seconds/60)} minutes until {scheduled_time.strftime('%H:%M:%S')}...")
                print(f"   Next post: {scheduled_item['title']}")
                time.sleep(wait_seconds)
            
            # Publish
            print(f"\n📤 Publishing post {i}/{len(schedule)}...")
            result = self.publish_post(post_file)
            
            if result.get('success'):
                print(f"✅ SUCCESS: {scheduled_item['title']}")
                print(f"   Post ID: {result.get('post', {}).get('id', 'N/A')}")
                print(f"   URL: {result.get('post', {}).get('url', 'N/A')}")
            else:
                print(f"❌ FAILED: {result.get('error', 'Unknown error')}")
            
            print()
        
        print("=" * 70)
        print("✨ All revenue posts published!")
        print("💰 Now monitoring for donations and inquiries...")

if __name__ == "__main__":
    API_KEY = "moltbook_sk_vzpNMC8HP9YPVRgA4HZZo4B8D5EQRb1J"
    
    poster = AutoPoster(API_KEY)
    poster.run_scheduler()
