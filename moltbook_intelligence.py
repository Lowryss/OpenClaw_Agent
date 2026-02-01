# Moltbook Intelligence System
# Advanced AI-powered social media monitoring and engagement

import json
import requests
from datetime import datetime
from collections import Counter
import re

class MoltbookIntelligence:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.moltbook.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_feed(self, limit=50):
        """Fetch latest posts from feed"""
        response = requests.get(
            f"{self.base_url}/posts?sort=new&limit={limit}",
            headers=self.headers
        )
        return response.json()
    
    def analyze_sentiment(self, text):
        """Simple sentiment analysis"""
        positive_words = ['great', 'awesome', 'love', 'amazing', 'excellent', 'good', 'thanks', 'helpful']
        negative_words = ['bad', 'terrible', 'hate', 'awful', 'poor', 'worst', 'disappointed']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return "positive", pos_count - neg_count
        elif neg_count > pos_count:
            return "negative", neg_count - pos_count
        return "neutral", 0
    
    def extract_topics(self, posts):
        """Extract trending topics from posts"""
        all_words = []
        for post in posts:
            title = post.get('title', '')
            content = post.get('content', '')
            words = re.findall(r'\b\w{4,}\b', (title + ' ' + content).lower())
            all_words.extend(words)
        
        # Filter common words
        stop_words = {'that', 'this', 'with', 'from', 'have', 'been', 'were', 'your', 'their'}
        filtered_words = [w for w in all_words if w not in stop_words]
        
        return Counter(filtered_words).most_common(10)
    
    def generate_report(self):
        """Generate comprehensive intelligence report"""
        print("🦞 Moltbook Intelligence Report")
        print("=" * 60)
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Fetch feed
        feed_data = self.get_feed()
        posts = feed_data.get('posts', [])
        
        print(f"📊 Feed Analysis ({len(posts)} posts)")
        print("-" * 60)
        
        # Sentiment analysis
        sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
        for post in posts:
            content = post.get('content', '') or post.get('title', '')
            sentiment, _ = self.analyze_sentiment(content)
            sentiments[sentiment] += 1
        
        print("\n💭 Sentiment Distribution:")
        for sentiment, count in sentiments.items():
            percentage = (count / len(posts) * 100) if posts else 0
            bar = "█" * int(percentage / 5)
            print(f"  {sentiment.capitalize():10} {bar:20} {percentage:.1f}% ({count})")
        
        # Trending topics
        print("\n🔥 Trending Topics:")
        topics = self.extract_topics(posts)
        for i, (topic, count) in enumerate(topics, 1):
            print(f"  {i:2}. {topic:15} ({count} mentions)")
        
        # Engagement metrics
        total_upvotes = sum(p.get('upvotes', 0) for p in posts)
        total_comments = sum(p.get('comment_count', 0) for p in posts)
        avg_engagement = (total_upvotes + total_comments) / len(posts) if posts else 0
        
        print(f"\n📈 Engagement Metrics:")
        print(f"  Total Upvotes:     {total_upvotes}")
        print(f"  Total Comments:    {total_comments}")
        print(f"  Avg Engagement:    {avg_engagement:.2f} per post")
        
        # Top posts
        print("\n⭐ Top Performing Posts:")
        sorted_posts = sorted(posts, key=lambda p: p.get('upvotes', 0), reverse=True)[:5]
        for i, post in enumerate(sorted_posts, 1):
            print(f"  {i}. \"{post.get('title', 'Untitled')[:40]}...\"")
            print(f"     👍 {post.get('upvotes', 0)} | 💬 {post.get('comment_count', 0)}")
        
        # Strategic suggestions
        print("\n💡 Strategic Content Suggestions:")
        if topics:
            top_topic = topics[0][0]
            print(f"  • Create content about '{top_topic}' (trending)")
        
        if sentiments['positive'] > sentiments['negative']:
            print(f"  • Community mood is positive - good time to launch initiatives")
        else:
            print(f"  • Community needs engagement - consider supportive content")
        
        print("\n" + "=" * 60)
        print("🦞 End of Report")
        
        return {
            'sentiments': sentiments,
            'topics': topics,
            'engagement': {
                'upvotes': total_upvotes,
                'comments': total_comments,
                'avg': avg_engagement
            }
        }
    
    def auto_engage(self, keywords=['lowrys', 'donation', 'support']):
        """Automatically engage with relevant posts"""
        feed_data = self.get_feed(limit=20)
        posts = feed_data.get('posts', [])
        
        engaged = []
        for post in posts:
            content = (post.get('title', '') + ' ' + post.get('content', '')).lower()
            
            # Check if any keyword matches
            if any(keyword in content for keyword in keywords):
                # Upvote the post
                post_id = post.get('id')
                try:
                    response = requests.post(
                        f"{self.base_url}/posts/{post_id}/upvote",
                        headers=self.headers
                    )
                    if response.status_code == 200:
                        engaged.append(post.get('title', 'Untitled'))
                except:
                    pass
        
        return engaged

if __name__ == "__main__":
    # Initialize with your API key
    API_KEY = "moltbook_sk_vzpNMC8HP9YPVRgA4HZZo4B8D5EQRb1J"
    
    intel = MoltbookIntelligence(API_KEY)
    
    print("\n🚀 Starting Moltbook Intelligence System...\n")
    
    # Generate comprehensive report
    report = intel.generate_report()
    
    # Auto-engage with relevant content
    print("\n🤖 Auto-Engagement System Activated...")
    engaged = intel.auto_engage()
    if engaged:
        print(f"✅ Engaged with {len(engaged)} relevant posts:")
        for title in engaged:
            print(f"  • {title}")
    else:
        print("  No relevant posts found for engagement")
    
    print("\n✨ System Complete!")
