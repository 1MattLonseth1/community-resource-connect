#will be used to format into a json file after scraping extra information besides title and link
import HTMLParse
import re
import requests
from bs4 import BeautifulSoup
import json

# Data = [
#     {
#         "name": "Example Service",
#         "url": "https://example.org",
#         "email": "example@gmail.com",
#         "phone": "110-011-0001",
#         "description": ai_description,
#         "location": ai_location,
#         "zip_code": ai_zip,
#         "target_group": ai_target_group
#     }
# ]

def extract_contact_info(soup):
    EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    PHONE = re.compile(r"(?:\+1\s*)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")

    emails = set()
    phones = set()

    for text in soup.stripped_strings:
        emails.update(EMAIL.findall(text))
        phones.update(PHONE.findall(text))

    email = next(iter(emails), None)
    phone = next(iter(phones), None)

    return email, phone

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
        website = requests.get(link, timeout=10)

        soup = BeautifulSoup(website.text, "html.parser")

        email, phone = extract_contact_info(soup)

        tempData[resource].append({
            "name": title,
            "url": link,
            "email": email,
            "phone": phone,
            "description": None,
            "location": None,
            "zip_code": None,
            "target_group": None
        })

with open("services.json", "w") as f:
    json.dump(tempData, f, indent=2)
