# DAG to update data for solar radiation
from airflow.decorators import dag, task
from settings import lat, lon, open_weathermap_key, db_engine, default_args
import requests
import pandas as pd


# Run DAG every hour starting at 01:00
@dag(default_args=default_args, schedule_interval="@hourly")
def update_solar():

    @task()
    def extract():

        url = f"http://api.openweathermap.org/data/2.5/solar_radiation/forecast?lat={lat}&lon={lon}&appid={open_weathermap_key}"
        res = requests.get(url)
        json_data = res.json()

        return json_data

    @task()
    def transform(data):

        # Load the key-values from the "list" key into a DataFrame
        df = pd.DataFrame(data["list"])
        # Extract the current date
        df["dates"] = pd.to_datetime(df["dt"], unit="s")
        # Extract the components values
        radiation = pd.json_normalize(df['radiation'][0])
        dfs = [df['dates'], radiation]
        merged_df = pd.concat(dfs, axis=1)
        # Get just the most recent values
        current = merged_df.head(n=1) 
        # Cast the cleaned values to a JSON array
        current_json = current.to_json(orient="records")

        return current_json

    @task()
    def load(cleaned_data):

        df = pd.read_json(cleaned_data, orient="records")
        # Convert the UNIX timestamps to datetimes
        df['dates'] = pd.to_datetime(df['dates'] / 1000, unit="s")
        # Write the cleaned data to the db schema
        df.to_sql(
            "solar_radiation", 
            db_engine, 
            method="multi", 
            index=False, 
            if_exists="append"
        )

    extract = extract()
    transform = transform(extract)
    load = load(transform)


update_solar_dag = update_solar()
