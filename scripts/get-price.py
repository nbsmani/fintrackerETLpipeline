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
import uuid
import pandas as pd

# Define API endpoint
url = 'https://api.gold-api.com'
headers = {"Content-Type": "application/json"}
symbol_file_path = "./data/symbols.csv"

# Load symbols from local csv. If the symbols file is not available, it can be fetched from the API and saved locally for future use.

if not os.path.isfile(symbol_file_path):
    print("Symbol file is not available. Getting symbols from `https://api.gold-api.com/symbols` and saving to local csv file.")
    
    # Make the API request to get symbols 
    # Set up headers for the API request
    
    try:   
        response = requests.get(f"{url}/symbols", headers=headers)
        if response.status_code == 200:
            data = response.json()
            data = pd.DataFrame(data)
            data.to_csv(symbol_file_path, index=False)
            symbols = data['symbol'].tolist()
            print(f"Symbols fetched and saved to {symbol_file_path}")
        else:
            print(f"Error fetching symbols: {response.status_code}")        
    # Handle potential errors
    except Exception as e:
        print(f"An error occurred: {e}")

else:
    symbols_data = pd.read_csv(symbol_file_path)
    symbols = symbols_data['symbol'].tolist()


# Initialize dictionary to hold current prices
current_price ={}
data = None

# Fetch current price for each symbol
for symbol in symbols:
    url_symbol = f"{url}/price/{symbol}"
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

#add a uuid for the extraction
current_price['uuid'] = str(uuid.uuid4())
current_price.to_csv(output_file, sep=',', index=False)

# Print confirmation message for logging
print(f"Price data saved to {output_file}")
