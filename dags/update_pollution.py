from airflow.decorators import dag, task
from datetime import datetime
import requests, os 
import pandas as pd


default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 5, 18),
    "retries": 1
}

# Get the API token from an environment variable 
token = os.getenv("TOKEN")

@dag(default_args=default_args, schedule_interval=None)
def update_pollution():

    # Extract data from API endpoint
    @task()
    def extract():

        req = requests.get(f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}")
        json_data = req.json()
        
        return json_data

    @task()
    def transform(data):

        # Load the key-values from the "list" key into a DataFrame
        df = pd.DataFrame(data["list"])
        # Extract the components values
        comps = pd.json_normalize(df['components'][0])
        # Extract the air quality index (AQI) value
        aqi = pd.json_normalize(df['main'][0])
        # Store the temporary dfs in a list
        dfs = [aqi, comps]
        # Combine the two DataFrames into a single df
        merged_df = pd.concat(dfs, axis=1)

        return merged_df


    extract = extract()
    transform = transform(extract)


update_pollution_dag = update_pollution()
