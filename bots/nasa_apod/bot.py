from tweepy import Client, OAuth1UserHandler, API
import requests
import schedule
import time
from datetime import datetime
from io import BytesIO

# Twitter API credentials
api_key = 
api_secret = 
bearer_token = 
access_token = 
access_token_secret = 

# NASA API key
nasa_api_key = 

def get_nasa_apod():
    nasa_url = f"https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}"
    try:
        response = requests.get(nasa_url)
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

# Schedule the job
schedule.every().day.at("09:35").do(post_apod)

# First post immediately
post_apod()

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute