import json

data = [
    {
        "name": "Example Service",
        "location": "Sample County",
        "url": "https://example.org",
        "source": "manual"
    }
]

with open("services.json", "w") as f:
    json.dump(data, f, indent=2)
