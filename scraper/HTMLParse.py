import GoogleSearch
import Fetch_html

resources = ['LGBTQ Resources NJ', 'Food Banks NJ', 
                'Single Parent Resources NJ', 'Homeless Resources NJ', 
                'Immigrant Resources NJ', 'Mental Health Resources NJ', 
                'Veteran Resources NJ', 'Disability Resources NJ'
                ]

def find():

    allFound = {}  # all resources found, keyed by title -> link

    for resource in resources:
        allFound[resource] = {}
        links = GoogleSearch.search(resource)

        for link in links:
            print(f"  Fetching: {link}")
            soup = Fetch_html.fetch_soup(link)

            if soup is None:
                continue  # already logged in fetch_html

            title = soup.title.text.strip() if soup.title else f"No Title | {link}"
            allFound[resource][title] = link
            print(f"  Found: {title}")

    return allFound