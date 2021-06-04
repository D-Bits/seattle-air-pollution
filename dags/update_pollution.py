from airflow.decorators import dag, task
from datetime import datetime
from settings import lat, lon, api_key, db_engine, default_args
import requests
import pandas as pd


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
        df['dates'] = pd.to_datetime(df['dates'] / 1000, unit="s")

        # Write the cleaned data to the db schema
        df.to_sql(
            "pollution", 
            db_engine, 
            method="multi", 
            index=False, 
            if_exists="append"
        )
        

    extract = extract()
    transform = transform(extract)
    load = load(transform)


update_pollution_dag = update_pollution()
