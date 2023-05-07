import os
import requests
from bs4 import BeautifulSoup
import boto3
import pandas as pd
import re
import glob

url = "https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
 
# Download the webpage content
response = requests.get(url)
page_content = response.text
 
# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(page_content, "html.parser")

# Creating list of dates we need
dates = ['2022.07', '2022.08', '2022.09', '2022.10', '2022.11', '2022.12']

#Find all anchor tags containing parquet file links
for i in dates:
    parquet_links_yellow = soup.find_all("a", href = re.compile(f".*/*yellow_tripdata_{i}.parquet"))
    parquet_links_green = soup.find_all("a", href = re.compile(f".*/*green_tripdata_{i}.parquet"))



    # Access each parquet URL, convert data to csv and save file to the specified destination folder
    for j in range (len(parquet_links_green)):
        parquet_url_green = parquet_links_green[j]["href"]
        parquet_url_yellow = parquet_links_yellow[j]["href"]
        
        df = pd.read_parquet(parquet_url_yellow)
        df.to_csv(f'taxi/Yellow_{i}.csv')
        print(f"Downloaded Yellow_tripdata {i}...")
        df = pd.read_parquet(parquet_url_green)
        df.to_csv(f'taxi/Green{i}.csv')
        print(f"Downloaded Green_tripdata {i}...")
 
print("All files have been downloaded.")


session = boto3.Session(aws_access_key_id= "", 
                        aws_secret_access_key='')
s3 = session.client('s3')

csv_files = glob.glob(os.path.join('taxi', "*.csv"))
 
for csv_file in csv_files:
    destination_path = os.path.join("uploaded", os.path.basename(csv_file))
 
    # Upload to Amazon S3
    s3.upload_file(csv_file, 'cis4400-group-project', os.path.basename(csv_file))
 
    print(f"Uploaded {csv_file} to S3")

print('Done')
