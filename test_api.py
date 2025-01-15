import os
from dotenv import load_dotenv
import requests

load_dotenv()
marketaux_api_key = os.getenv('MARKETAUX_API_KEY')

def test_api_parameters():
    base_url = "https://api.marketaux.com/v1/news/all"
    
    # Test different parameter combinations
    test_params = [
        {
            'name': "Basic Test",
            'params': {
                'api_token': marketaux_api_key,
                'language': 'en'
            }
        },
        {
            'name': "Source Domain Only",
            'params': {
                'api_token': marketaux_api_key,
                'language': 'en',
                'sources': 'wsj.com'  # Testing single source first
            }
        },
        {
            'name': "Entity Only",
            'params': {
                'api_token': marketaux_api_key,
                'language': 'en',
                'entities': 'Tesla'  # Testing single entity
            }
        }
    ]
    
    for test in test_params:
        try:
            print(f"\n\nTesting: {test['name']}")
            print(f"Parameters: {test['params']}")
            response = requests.get(base_url, params=test['params'])
            print(f"Full URL: {response.url}")
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('data'):
                    print("\nFirst article:")
                    article = data['data'][0]
                    print(f"Title: {article['title']}")
                    print(f"Source: {article['source']}")
            else:
                print(f"Error response: {response.text}")
                
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    print("Starting API parameter tests...")
    test_api_parameters()