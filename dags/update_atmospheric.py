# DAG to update data for atmospheric data (rainfall, humidity, etc.)
# over the past 24 hrs. 
from datetime import datetime, timedelta
from os import getenv
from airflow.decorators import dag, task
from settings import db_engine, default_args, weatherapi_key
import requests
import pandas as pd


# Define global variables
start = datetime.today() - timedelta(days=1)
start_unix = start.timestamp()
end = datetime.now().timestamp()


@dag(default_args=default_args, schedule_interval="@hourly")
def update_rainfall():

    # Extract data from API endpoint
    @task()
    def extract():

        req = requests.get(f"https://api.weatherapi.com/v1/current.json?key={weatherapi_key}&q=Seattle&aqi=yes")
        json_data = req.json()
        
        return json_data
