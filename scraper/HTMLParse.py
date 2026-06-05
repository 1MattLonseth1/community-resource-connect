import GoogleSearch
import Fetch_html



def find(resources):

    allFound = {}  #all resources, title -> link

    for resource in resources:
        allFound[resource] = {}
        links = GoogleSearch.search(resource)

        for link in links:
            print(f"  Fetching: {link}")
            soup = Fetch_html.fetch_soup(link)

            if soup is None:
                continue

            title = soup.title.text.strip() if soup.title else f"No Title | {link}"
            allFound[resource][title] = link
            print(f"  Found: {title}")

    return allFound