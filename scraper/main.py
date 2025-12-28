import json

# Data = [   WHAT THE DATA WILL LOOK LIKE
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

data = {}

with open("services.json", "w") as f:
    json.dump(data, f, indent=2)



with open("services.json", "r") as f:
    newData = json.load(f)

print(newData)
