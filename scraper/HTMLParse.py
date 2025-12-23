import re
import requests
import GoogleSearch
from bs4 import BeautifulSoup



resources = ['LGBTQ Resources NJ', 'Food Banks NJ', 'Single Parent Resources NJ', 'Homeless resouces nj']

allFound = {} #all resources found and put into dictionary for later parsing

for resource in resources:
    allFound[resource] = {}
    links = GoogleSearch.search(resource)
    for link in links:
        response = requests.get(link)
        
        if response.status_code != 200:
                allFound[resource][link] = link
                continue
        
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        if soup.title: #has title
            title = soup.title.text.strip()
        else: #does not have title tag
            title = "Untitled Page"
        
        allFound[resource][title] = link