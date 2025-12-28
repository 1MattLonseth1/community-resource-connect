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
    
    allFound = {} #all resources found and put into dictionary for later parsing

    for resource in resources:
        allFound[resource] = {}
        links = GoogleSearch.search(resource)
        for link in links:
            response = requests.get(link, timeout=10)
            
            if response.status_code != 200:
                continue
            
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            if soup.title: #has title
                title = soup.title.text.strip()
            else: #does not have title tag
                title = "No Title | " + link
            
            allFound[resource][title] = link
    
    return allFound