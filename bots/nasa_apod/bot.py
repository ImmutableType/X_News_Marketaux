import os
from tweepy import Client, OAuth1UserHandler, API
import requests
from datetime import datetime
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials from environment variables
api_key = os.getenv('TWITTER_API_KEY')
api_secret = os.getenv('TWITTER_API_SECRET')
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_SECRET')
nasa_api_key = os.getenv('NASA_API_KEY')

def get_nasa_apod():
    nasa_url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}"
    try:
        response = requests.get(nasa_url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error getting APOD: {str(e)}")
        return None

def post_apod():
    try:
        # Set up Twitter authentication for media upload
        auth = OAuth1UserHandler(
            api_key, api_secret,
            access_token, access_token_secret
        )
        api = API(auth)
        
        # Get APOD data
        apod_data = get_nasa_apod()
        
        if apod_data:
            # Download the image
            image_response = requests.get(apod_data['url'])
            image_response.raise_for_status()
            image = BytesIO(image_response.content)
            
            # Upload media to Twitter
            media = api.media_upload(filename='apod.jpg', file=image)
            
            # Create tweet text
            title = apod_data.get('title', 'NASA APOD')
            
            # Initialize client for tweeting
            client = Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
                bearer_token=bearer_token
            )
            
            # Post tweet with media
            response = client.create_tweet(
                text=f"🔭 NASA Astronomy Picture of the Day\n\n{title}",
                media_ids=[media.media_id]
            )
            
            print(f"Tweet posted successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}!")
            print(f"Tweet ID: {response.data['id']}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

# When running in GitHub Actions, we don't need the scheduler
if __name__ == "__main__":
    post_apod()