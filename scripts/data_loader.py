#data_loader.py

#import necessary libraries
import os
import sys
import pandas as pd
from sqlalchemy import create_engine, URL

#Input_params
input_file = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
host = sys.argv[4]
port = sys.argv[5]
database = sys.argv[6]
schema = sys.argv[7]
table_name = sys.argv[8]

#Read CSV file into DataFrame
#for debugging purpose, print the files in the input directory
files = os.listdir(os.path.dirname(input_file))
print(f"Files in input directory: {files}")
#read the input file into a dataframe and convert column names to lowercase for consistency
df = pd.read_csv(input_file)
df.columns = [x.lower() for x in df.columns]
print (df.head()) #for debugging purpose, print the first few rows of the dataframe to verify the data is read correctly
#Create connection engine to Postgres

dbms_url = URL.create(
    drivername='postgresql',
    username=username,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = create_engine(dbms_url, echo=False)
try:
    df.to_sql(name = table_name, 
        con=engine,
        schema=schema,
        if_exists='append', 
        index=False)
    print(f"Data ingested successfully into {schema}.{table_name} table.")
except Exception as e:
    print(f"Error occurred during data ingestion: {e}")
