from airflow.decorators import dag, task
from datetime import datetime
from sqlalchemy import create_engine
import requests, os 
import pandas as pd


default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 5, 18),
    "retries": 1
}

# Get the API token from an environment variable 
api_key = os.getenv("API_KEY")
# Set latitude and longitude for Seattle
lat = 47.6062
lon = -122.3321

# Create SQL Alchemy engine for loading data
db_engine = create_engine(os.getenv("DB_CONN"))

# Run DAG every hour starting at 01:00
@dag(default_args=default_args, schedule_interval="@hourly")
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
        # Extract the current date
        df["dates"] = pd.to_datetime(df["dt"], unit="s")
        # Extract the components values
        comps = pd.json_normalize(df['components'][0])
        # Extract the air quality index (AQI) value
        aqi = pd.json_normalize(df['main'][0])
        # Store the temporary dfs in a list
        dfs = [df["dates"], aqi, comps]
        # Combine the DataFrames list into a single df
        merged_df = pd.concat(dfs, axis=1)
        json_df = merged_df.to_json(orient="records")

        return json_df

    @task()
    def load(cleaned_data):

        df = pd.read_json(cleaned_data)
        # Convert the UNIX timestamps to datetimes
        df["dates"] = pd.to_datetime(df["dates"])
        df.to_sql("pollution", db_engine, method="multi", index=False, if_exists="append")


    extract = extract()
    transform = transform(extract)
    load = load(transform)


update_pollution_dag = update_pollution()
