import json

Data = [
    {
        "name": "Example Service",
        "url": "https://example.org",
        "email": "example@gmail.com",
        "phone": "110-011-0001"
    }
]



with open("services.json", "w") as f:
    json.dump(data, f, indent=2)



with open("services.json", "r") as f:
    newData = json.load(f)

print(newData)
