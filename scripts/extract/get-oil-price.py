import requests

response = requests.get(
    'https://api.oilpriceapi.com/v1/demo/prices'
)
print(response.json())
