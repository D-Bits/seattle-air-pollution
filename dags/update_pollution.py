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

        # Load JSON stored in the "list" key into DataFrame
        df = pd.DataFrame(data["list"])
        # Extract, and normalize, the values from the "components" key
        comps = pd.json_normalize(dict(df['components'][0]))
        

    extract = extract()
    transform = transform(extract)


update_pollution_dag = update_pollution()
