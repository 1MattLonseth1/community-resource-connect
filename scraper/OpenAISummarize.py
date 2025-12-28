from openai import OpenAI
import json
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)

with open("services.json", "r") as f:
    data = json.load(f) #services dictionary

for broad_resource, specific_resources in data.items():
    #broad resource is the "Food Banks NJ", etc
    #specific resource is the list where each index contains 4 keys about that specific resource
    for item in specific_resources: #should iterate through the list
        link = item['url']
        
        #use ai to go to the link, summarize the service, location, zip code, target group
        #ask it to return where index 0 = summary, index 1 = location, so i can easily add to json file.

with open("services.json", "w") as f:
    json.dump(data, f, indent=2)