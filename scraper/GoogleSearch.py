import requests

API_KEY = None#need to add back
SE_ID = None #need to add back

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
