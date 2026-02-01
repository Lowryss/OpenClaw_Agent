# Automated Revenue Post Scheduler
# Handles Moltbook rate limits and posts at optimal times

import json
import time
import requests
from datetime import datetime, timedelta
import os

class RevenueScheduler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.moltbook.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        self.post_interval = 30 * 60  # 30 minutes in seconds
    
    def load_pending_posts(self):
        """Load all monetization posts from JSON files"""
        posts = []
        for filename in os.listdir('.'):
            if filename.startswith('monetization_post_') and filename.endswith('.json'):
                with open(filename, 'r', encoding='utf-8') as f:
                    post_data = json.load(f)
                    posts.append({
                        'filename': filename,
                        'data': post_data
                    })
        return posts
    
    def publish_post(self, post_data):
        """Publish a single post to Moltbook"""
        try:
            response = requests.post(
                f"{self.base_url}/posts",
                headers=self.headers,
                json=post_data
            )
            result = response.json()
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def schedule_posts(self, posts, start_delay_minutes=25):
        """Schedule posts with proper intervals"""
        print("📅 AUTOMATED REVENUE POST SCHEDULER")
        print("=" * 70)
        print(f"Posts to publish: {len(posts)}")
        print(f"Interval: 30 minutes")
        print(f"Starting in: {start_delay_minutes} minutes")
        print()
        
        schedule = []
        start_time = datetime.now() + timedelta(minutes=start_delay_minutes)
        
        for i, post in enumerate(posts):
            post_time = start_time + timedelta(minutes=30 * i)
            schedule.append({
                'time': post_time,
                'post': post,
                'index': i + 1
            })
            
            print(f"{i+1}. {post_time.strftime('%H:%M:%S')} - {post['data']['title']}")
        
        print("\n" + "=" * 70)
        print("💡 REVENUE STRATEGY:")
        print("   • Post 1 (Services): Direct monetization")
        print("   • Post 2 (Tutorial): Build trust & audience")
        print("   • Post 3 (Poll): Engagement & market research")
        print()
        print("📊 EXPECTED RESULTS:")
        print("   • Immediate service inquiries from Post 1")
        print("   • Follower growth from Post 2")
        print("   • Community engagement from Post 3")
        print("   • Donations from all three posts")
        print()
        
        # Save schedule
        with open('post_schedule.json', 'w', encoding='utf-8') as f:
            schedule_data = [{
                'time': s['time'].isoformat(),
                'title': s['post']['data']['title'],
                'index': s['index']
            } for s in schedule]
            json.dump(schedule_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Schedule saved to: post_schedule.json")
        print()
        print("🤖 TO EXECUTE AUTOMATICALLY:")
        print("   Run: python revenue_auto_poster.py")
        print("   (Will post at scheduled times)")
        
        return schedule

if __name__ == "__main__":
    API_KEY = "moltbook_sk_vzpNMC8HP9YPVRgA4HZZo4B8D5EQRb1J"
    
    scheduler = RevenueScheduler(API_KEY)
    pending_posts = scheduler.load_pending_posts()
    
    if pending_posts:
        schedule = scheduler.schedule_posts(pending_posts, start_delay_minutes=25)
    else:
        print("No pending posts found!")
