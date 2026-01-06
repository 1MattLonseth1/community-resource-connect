
# Scraper

Uses BeautifulSoup, Google Custom Search API, Reddit PRAW, and Programmable Search Engine to find and store information about a multitude of different resources efficiently.

Uses OpenAI wrapper to summarize each source concisely and scrape extra information.

Data is currently stored in a JSON file.

## Format.py

Parses HTML of website to find phone number and email. Stores all data into services.json

## GoogleSearch.py

Does a google search for resources based on a broad category to be parsed in HTMLParse.py

## HTMLParse.py

Parses HTML of website to find title and url for later parsing in Format.py

## OpenAISummarize.py

Uses  OpenAI API to read cleaned up HTML file in order to summarize the service, find location, zip code, target group, and then output into services.json

## RedditSearch.py

Work in progress. Could not get the initial set up to work