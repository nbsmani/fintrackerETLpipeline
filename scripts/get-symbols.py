"""
Script to fetch financial symbols from an external API and save them to a JSON file.
The ApI endpoint used is 'https://api.gold-api.com/symbols'. It has unlimited free access for fetching real-time data.
The symbols data is saved to a local JSON file located at './data/symbols.json'. 
This script is intended to be run prior to executing the `get-price.py` script to ensure that the latest symbols are available for price fetching.

Developed by: Balasubramaniam Namasivayam
Date: 2025-06-15
"""

# import necessary libraries
import os
import requests
import json

# Define API endpoint and headers
url= "https://api.gold-api.com/symbols"
headers= {
        "Content-Type": "application/json"}

# Make the API request to get symbols 
try:   
    response= requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        output_file = './data/symbols.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"Symbols data saved to {output_file}")
# Handle potential errors
except Exception as e:
    print(f"An error occurred: {e}")
