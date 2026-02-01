"""
Script to fetch financial symbols from an external API and save them to a JSON file.
The ApI endpoint used is 'https://api.gold-api.com/symbols'. It has unlimited free access for fetching real-time data.
The symbols data is saved to a local JSON file located at './data/symbols.json'. 
This script is intended to be run prior to executing the `get-price.py` script to ensure that the latest symbols are available for price fetching.

Developed by: Balasubramaniam Namasivayam
Date: 15/06/2025
"""

# import necessary libraries
import os
import requests
import json

# Define API endpoint and headers
url= "https://api.gold-api.com/symbols"
headers= {
        "Content-Type": "application/json"}

# Define output file path
output_file = './data/symbols.json'

#check if symbols file already exists
if os.path.exists(output_file):
    print(f"Symbols file already exists at {output_file}. To update, please delete the existing file and rerun the script.")
    exit()

# Make the API request to get symbols 
try:   
    response= requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"Symbols data saved to {output_file}")
# Handle potential errors
except Exception as e:
    print(f"An error occurred: {e}")
