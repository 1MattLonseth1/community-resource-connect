import json
import os
import Fetch_html
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)


def safe_json_parse(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
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
    "canonical_name": str or null,
    "description": str,
    "location": str or null,
    "zip_code": str or null,
    "target_group": str or null
    }}
    Rules:
    - Do NOT guess
    - "description" value should be maximum 4 sentences
    - If unknown, use null (not the string "None")
    - No extra text outside JSON
    """

    DEFAULT_AI_DATA = {
        "canonical_name": None,
        "description": None,
        "location": None,
        "zip_code": None,
        "target_group": None
    }

    try:
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

        if parsed and isinstance(parsed, dict):
            for key in ai_data:
                if key in parsed:
                    val = parsed[key]
                    # Normalize the string "None" or "null" to actual None
                    if isinstance(val, str) and val.strip().lower() in ("none", "null", ""):
                        val = None
                    ai_data[key] = val

        return ai_data

    except Exception as e:
        print(f"  AI summarization failed: {e}")
        return DEFAULT_AI_DATA.copy()


def extract_page_text(soup, max_chars=6000):
    texts = []
    for tag in soup.find_all(["p", "li", "h1", "h2", "h3"]):
        text = tag.get_text(strip=True)
        if len(text) > 30:
            texts.append(text)
    combined = " ".join(texts)
    return combined[:max_chars]


with open("services.json", "r") as f:
    data = json.load(f)

for broad_resource, specific_resources in data.items():
    print(f"\nProcessing: {broad_resource}")
    for item in specific_resources:
        link = item.get('url')
        if not link:
            print(f"  Skipping item with no URL: {item.get('name')}")
            continue

        soup = Fetch_html.fetch_soup(link)
        if soup is None:
            continue  # already logged by fetch_html

        page_text = extract_page_text(soup)
        if not page_text:
            print(f"  No text extracted from {link}")
            continue

        print(f"  Summarizing: {item.get('name', link)}")
        ai_data = ai_summarize_service(page_text)

        if ai_data.get("canonical_name"):
            item["name"] = ai_data["canonical_name"]

        item.update({k: v for k, v in ai_data.items() if k != "canonical_name"})

with open("services.json", "w") as f:
    json.dump(data, f, indent=2)

print("\nDone. services.json updated.")