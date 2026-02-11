#data_loader.py

#import necessary libraries
import os
import sys
import pandas as pd
from sqlalchemy import create_engine, URL, text
import uuid

#Input_params
input_dir = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
host = sys.argv[4]
port = sys.argv[5]
database = sys.argv[6]
schema = sys.argv[7]
table_name = sys.argv[8]
archive_dir = sys.argv[9]
#list the csv files and read CSV file into DataFrame
files =[f for f in os.listdir(input_dir) if '.csv' in f] 

#for debugging purpose, print the files in the input directory
print(f"Files in input directory: {files}")

##check if the archive directory exists, if not create it
if not os.path.exists(archive_dir):
    os.makedirs(archive_dir)

##Create db connection for ingestion into Postgres

dbms_url = URL.create(
        drivername='postgresql',
        username=username,
        password=password,
        host=host,
        port=port,
        database=database
    )

engine = create_engine(dbms_url, echo=False)




#function to verify if there is `uuid` column in the dataframe, if not add a new column with uuid values
def assign_uuid(df):
    if 'uuid' not in df.columns:
        df['uuid'] = str(uuid.uuid4())
    return df

# Fucntion to truncate the bronze table before loading the data
def truncate_table():
    with engine.connect() as connection:
        connection.execute(text(f"TRUNCATE TABLE {schema}.{table_name}"))
        connection.commit()
        print(f"Table {schema}.{table_name} is truncated successfully.")

def process_file(file):
    input_file = os.path.join(input_dir, file)
    print(f"Processing file: {input_file}")
    #read the input file into a dataframe and convert column names to lowercase for consistency
    df = pd.read_csv(input_file)
    df.columns = [x.lower() for x in df.columns]
    #add uuid column if not exists
    df = assign_uuid(df) # this function will backfill the uuid for some files which are missing the uuid column, for the files which already have uuid column, it will not change the existing values. This is to ensure that we have a unique identifier for each record in the dataframe, which can be useful for tracking and debugging purposes.
    try:
        df.to_sql(name = table_name, 
            con=engine,
            schema=schema,
            if_exists='append', 
            index=False)
        print(f"Data ingested successfully into {schema}.{table_name} table.")
        #move the processed file to archive directory
        os.rename(input_file, os.path.join(archive_dir, file))
        print(f"File {file} is processed and moved to archive directory.")
    
    except Exception as e:
        print(f"Error occurred during data ingestion: {e}")
    
if __name__ == "__main__":
    #truncate the bronze table before loading the data
    truncate_table() 

#process each file in the input directory
    for file in files: 
        process_file(file)
