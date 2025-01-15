import os
from tweepy import Client, OAuth1UserHandler, API
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment variables
api_key = os.getenv('TWITTER_API_KEY')
api_secret = os.getenv('TWITTER_API_SECRET')
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_SECRET')
marketaux_api_key = os.getenv('MARKETAUX_API_KEY')

def get_market_news():
    marketaux_url = f"https://api.marketaux.com/v1/news/all?api_token={marketaux_api_key}&language=en"
    try:
        response = requests.get(marketaux_url)
        response.raise_for_status()
        data = response.json()
        return data['data'][:3]  # Get top 3 news items for the thread
    except Exception as e:
        print(f"Error getting news: {str(e)}")
        return None

def create_thread_text(news_items):
    thread_texts = []
    
    # Create opening tweet
    thread_texts.append("🚨 Latest Market News Update 📈\n\nTop stories:")
    
    # Add news items
    for item in news_items:
        text = (f"📰 {item['title']}\n\n"
                f"{item['description'][:100]}...\n\n"
                f"Source: {item['source']}")
        thread_texts.append(text)
    
    return thread_texts

def post_thread():
    try:
        # Initialize client for tweeting
        client = Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            bearer_token=bearer_token
        )
        
        # Get news data
        news_items = get_market_news()
        
        if news_items:
            # Create thread texts
            thread_texts = create_thread_text(news_items)
            
            # Post initial tweet
            previous_tweet_id = None
            for i, text in enumerate(thread_texts):
                if i == 0:
                    response = client.create_tweet(text=text)
                    previous_tweet_id = response.data['id']
                else:
                    response = client.create_tweet(
                        text=text,
                        in_reply_to_tweet_id=previous_tweet_id
                    )
                    previous_tweet_id = response.data['id']
            
            print(f"Thread posted successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}!")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    post_thread()