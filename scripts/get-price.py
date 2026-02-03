"""
PROJECT: Real-Time Commodity Price Ingestion
DESCRIPTION:
    This script performs an automated data ingestion process to fetch 
    current market prices for a specific list of financial symbols.

PROCESS FLOW:
    1. EXTRACT: 
       - Loads a target list of symbols (e.g., XAU, XAG) from a local JSON file.
       - Iteratively queries the Gold-API for each symbol's real-time data.
    2. TRANSFORM:
       - Handles API connection errors by assigning "NA" placeholders.
       - Generates a dynamic timestamp for the filename, prioritizing the 
         API's 'updatedAt' field, falling back to system time if unavailable.
       - Normalizes the nested JSON responses into a tabular Pandas DataFrame.
    3. LOAD:
       - Ensures a local 'landing_zone' directory exists.
       - Saves the structured data into a CSV file for downstream analysis.

OUTPUT: 
    A CSV file located in ./data/landing_zone/ with the naming convention:
    priceYYYY-MM-DD-HH-MM-SS.csv
Author: Balasubramaniam Namasivayam
Date: 15/06/2025
"""

# Import necessary libraries
import os
from datetime import datetime
import requests
import json
import pandas as pd

# Define API endpoint
url = 'https://api.gold-api.com/price/'
symbol_file_path = "./data/symbols.json"
# Load symbols from local JSON file. If the symbols file is not available, it can be created by running `./scripts/get-symbols.py`
if symbol_file_path:
    with open("./data/symbols.json", 'r') as f:
        symbols_data = json.load(f)
    symbols_data = pd.DataFrame(symbols_data)
    symbols = symbols_data['symbol'].tolist()

else:
    print("Symbol file is not available. Please run `./scripts/get-symbols.py` to create the symbols file.")

# Set up headers for the API request
headers = {
    "Content-Type": "application/json"}

# Initialize dictionary to hold current prices
current_price ={}
data = None

# Fetch current price for each symbol
for symbol in symbols:
    url_symbol = f"{url}{symbol}"
    response = requests.get(url_symbol, headers=headers)
    if response.status_code == 200:
        data = response.json()
        current_price[symbol] = data
    else:
        print(f"Error fetching price for {symbol}: {response.status_code}")
        current_price[symbol] = "NA"

# Validate timestamp
# This uses the timestamp from the last successful API call in the loop
if data and data['updatedAt']:
    latest_time = data["updatedAt"].replace(":", "-")
else:
    # Fallback to system time if API timestamp is unavailable
    latest_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

#Ensure landing zone directory exists before saving the output file
os.makedirs('./data/landing_zone/', exist_ok=True)
output_file = f'./data/landing_zone/price{latest_time}.csv'

# Convert the current price dictionary to a DataFrame and load as CSV
current_price = pd.DataFrame.from_dict(current_price, orient='index')
current_price.to_csv(output_file, sep=',', index=False)

# Print confirmation message for logging
print(f"Price data saved to {output_file}")