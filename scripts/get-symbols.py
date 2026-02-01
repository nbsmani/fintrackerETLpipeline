import os
import requests
import json

url= "https://api.gold-api.com/symbols"

headers= {
        "Content-Type": "application/json"}
    
response= requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")

output_file = './data/symbols.json'
with open(output_file, 'w') as f:
    json.dump(data, f, indent=4)
print(f"Symbols data saved to {output_file}")

