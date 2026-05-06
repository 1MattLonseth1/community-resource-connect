import re
import requests
import GoogleSearch
from bs4 import BeautifulSoup

resources = ['LGBTQ Resources NJ', 'Food Banks NJ', 
                'Single Parent Resources NJ', 'Homeless Resources NJ', 
                'Immigrant Resources NJ', 'Mental Health Resources NJ', 
                'Veteran Resources NJ', 'Disability Resources NJ'
                ]

def find():
    
    allFound = {} #all resources found and put title and link into dictionary for later parsing

    for resource in resources:
        allFound[resource] = {}
        links = GoogleSearch.search(resource)
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html",
            "Accept-Language": "en-US,en;q=0.9"
        }
        
        for link in links:
            try:
                response = requests.get(link, headers=headers, timeout=10)
                if response.status_code == 200:
                    break;
                else:
                    print(f"Failed: {link} (status {response.status_code})")
            except requests.exceptions.RequestException as e:
                print(f"Error with {link}: {e}")
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            if soup.title: #has title
                title = soup.title.text.strip()
            else: #does not have title tag
                title = "No Title | " + link
            
            allFound[resource][title] = link
    
    return allFound