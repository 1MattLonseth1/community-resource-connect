
Uses BeautifulSoup, Google Custom Search API, and Programmable Search Engine to find and store information about a multitude of different resources efficiently



The following are notes on BeautifulSoup

from bs4 import BeautifulSoup #import beautifulsoup to use

with open("index.html", "r") as f:  ## opens html file
    doc = BeautifulSoup(f, "html.parser") # allows you to read into a hmtl file, can just print doc

#when looking for some time of information: can look at the specific html tags like title or <p>
# add .string to make only the text show not the tag
# can al
tag = doc.title #first thing tagged title, .find_all will find everything with that tag, indexing will allow you find a specific tag
print(tag.string) 
tag.string = "hello" # replaces first title with hello

#html from website

import requests
url = "website you want to access"
result = requests.get(url)
result.text # <<<< read from this

prices = doc.find_all(string="$") #to find specific text, need to acess the parent of the text to see where that text comes from
# everything in BS is in a tree like structure, by nested div tags
parent = prices[0].parent

#.find() = first result, .find_all() all results with that tag/text, #tag.attrs prints all the attributes
# can put a list of tags into find_all to give you all the things will those tags, can narrow down speicfic tags as "tag, string"
# to modify attributes of a tag, edit and add like a dictionary

import re #allows you to scan/skip the parent = prices[0].parent / gives you the text surounding text you search for
prices = doc.find_all(string=re.compile("\$.*")) #then do .strip to format correctly, can add limit to limit number of results

#just write into a new file to save chnages, .write(str(doc))

#to access siblings / things at the same 'level' in the tree. 
tbody = doc.tbody #-> the tag I am looking at that contains all the rows
trs = tbody.contents #-> all the things that has the parent tbody, can then to trs[0].next_sibling(s)/.previous_sibling(s) or just iterate through them
# .name = name of tag
#finding prices of crypto
for tr in trs: #each row in all rows t
    for td in tr.contents[2:4]: #contents of each row
        print(td)

#Google custom search api