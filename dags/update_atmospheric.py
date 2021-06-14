# DAG to update data for atmospheric data (rainfall, humidity, etc.)
# over the past 24 hrs. 
from airflow.decorators import dag, task
from settings import db_engine, default_args, weatherapi_key
import pandas as pd
import requests


@dag(default_args=default_args, schedule_interval="@hourly")
def update_atmospheric():

    # Extract data from API endpoint
    @task()
    def extract():

        req = requests.get(f"https://api.weatherapi.com/v1/current.json?key={weatherapi_key}&q=Seattle&aqi=yes")
        json_data = req.json()
        
        return json_data

    @task()
    def transform(data):

        df = pd.DataFrame(data['current'])
        # Drop unnessecary fields
        cleaned_df = df.drop([
            'last_updated_epoch', 
            'temp_f',
            'is_day',
            'condition',
            'wind_mph',
            'wind_degree',
            'wind_dir',
            'pressure_in',
            'precip_in',
            'feelslike_f',
            'feelslike_c',
            'vis_miles',
            'uv',
            'gust_mph',
            'gust_kph',
            'air_quality'
        ], axis=1)

        # Extract only the most recent record
        current = cleaned_df.head(n=1)
        # Cast the df to a JSON array
        cleaned_json = current.to_json(orient="records")

        return cleaned_json

    @task()
    def load(cleaned_data):

        df = pd.read_json(cleaned_data, orient="records")
        # Write the cleaned data to the db schema
        df.to_sql(
            "atmospheric", 
            db_engine, 
            method="multi", 
            index=False, 
            if_exists="append"
        )

    extract = extract()
    transform = transform(extract)
    load = load(transform)


update_atmospheric_dag = update_atmospheric()
