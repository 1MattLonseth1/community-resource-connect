import requests
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('GOOGLE_API_KEY') # type: ignore #need to add back
SE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID') # type: ignore #need to add back

url = 'https://www.googleapis.com/customsearch/v1'

def search(term):
    search_query = term #'Food Banks NJ'

    params = {
    'q': search_query,
    'key': API_KEY,
    'cx': SE_ID,
    }

    response = requests.get(url, params=params)
    results = response.json()
    
    links = []
    for item in results.get("items", []):
        links.append(item["link"])
    return links
