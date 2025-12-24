#will be used to format into a json file after scraping extra information besides title and link
import HTMLParse
import re
import requests
from bs4 import BeautifulSoup
import json

resources = ['LGBTQ Resources NJ', 'Food Banks NJ', 
                'Single Parent Resources NJ', 'Homeless Resources NJ', 
                'Immigrant Resources NJ', 'Mental Health Resources NJ', 
                'Veteran Resources NJ', 'Disability Resources NJ'
                ]

tempData = {}

found = HTMLParse.find()
for resource in resources:
    i=0
    tempData[resource] = []
    for title, link in found[resource].items():
        website = requests.get(link)

        soup = BeautifulSoup(website.text, "html.parser")

        emails = soup.find_all(string=re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"))
        email = emails[0].strip() if emails else None

        phones = soup.find_all(string=re.compile(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"))
        phone = phones[0].strip() if phones else None
        
        tempData[resource].append({
            "name": title,
            "url": link,
            "email": email,
            "phone": phone
        })

with open("services.json", "w") as f:
    json.dump(tempData, f, indent=2)

        





