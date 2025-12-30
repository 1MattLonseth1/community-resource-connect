from openai import OpenAI
import json
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)

def safe_json_parse(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Attempt to extract JSON object from text
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
    return None


def ai_summarize_service(page_text):
    prompt = f"""
    You are extracting structured information about a public service.

    Using ONLY the information below, return valid JSON.

    TEXT:
    \"\"\"
    {page_text}
    \"\"\"

    Return ONLY valid JSON in this format:
    {{
    "canonical_name": str or None,
    "description": str,
    "location": str or None,
    "zip_code": str or None,
    "target_group": str or None
    }}
    Rules:
    - Do NOT guess
    - "description" value should be maximum 4 sentences
    - If unknown, use None
    - No extra text outside JSON
    """

    DEFAULT_AI_DATA = {
    "canonical_name": None,
    "description": None,
    "location": None,
    "zip_code": None,
    "target_group": None
    }

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You extract factual data from text and return strict JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    raw = response.choices[0].message.content.strip()
    parsed = safe_json_parse(raw)

    ai_data = DEFAULT_AI_DATA.copy()
    
    if parsed:
        for key in ai_data:
            if key in parsed and parsed[key] is not None:
                ai_data[key] = parsed[key]
                
    return ai_data


def extract_page_text(soup, max_chars=6000):
    texts = []

    for tag in soup.find_all(["p", "li", "h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if len(text) > 30:
            texts.append(text)

    combined = " ".join(texts)
    return combined[:max_chars]  # hard cap for cost control



with open("services.json", "r") as f:
    data = json.load(f) #services dictionary

for broad_resource, specific_resources in data.items():
    #broad resource is the "Food Banks NJ", etc
    #specific resource is the list where each index contains 8 keys about that specific resource
    for item in specific_resources: #should iterate through the list
        link = item['url']
    
        response = requests.get(link, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        page_text = extract_page_text(soup)
        if not page_text:
            continue

        ai_data = ai_summarize_service(page_text)

        if ai_data.get("canonical_name"):
            item["name"] = ai_data["canonical_name"]

        item.update({k: v for k, v in ai_data.items() if k != "canonical_name"})

    #use ai to read cleaned up HTML file, summarize the service, location, zip code, target group, output into JSON formatting

with open("services.json", "w") as f:
    json.dump(data, f, indent=2)