import os
import requests

api_path = './assets/.api'

def make_api_request():
    if os.path.isfile(api_path):
        with open(api_path, 'r') as file:
            API_KEY = file.read().strip()
    else:
        raise FileNotFoundError(f"API key file not found at {api_path}.")
    symbol = "XAU"
    currency = "EUR"
    date = ""
    url = f"https://www.goldapi.io/api/{symbol}/{currency}{date}"
    headers = {
        'x-access-token': API_KEY,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.text
        return(result)
    except requests.exceptions.RequestException as e:
        print("Error:", str(e))
    
result=make_api_request()