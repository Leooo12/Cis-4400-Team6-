from io import StringIO
import requests
import pandas as pd


a = [40.68948814, 40.61079107, 40.86574543, 40.72413721, 40.55066537]
b = [-74.17152568, -73.82248951, -73.84494664, -73.97772563, -74.18753677]
# API and parameters
for i in range (len(a)):
    lat = a[i]
    long = b[i]
    api_url = (f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={long}&start_date=2022-07-01&end_date=2022-12-31&hourly=temperature_2m,weathercode")
    
    # Query the API with parameters
    response = requests.get(api_url)
    response_data = response.json()

    # Convert the response to a DataFrame
    data = pd.DataFrame(response_data)
    data.to_csv(f"response{i}.csv")

    # Save the DataFrame as a CSV file in memory
    csv_buffer = StringIO()
    les = data.to_csv(csv_buffer, index=False)
 