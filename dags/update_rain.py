# DAG to update data for rainfall. Each DAG run collects aggregate rainfall
# over the past 24 hrs. 
from datetime import datetime, timedelta
from airflow.decorators import dag, task
from settings import lat, lon, api_key, db_engine, default_args
import requests
import pandas as pd


# Define global variables
start = datetime.today() - timedelta(days=1)
start_unix = start.timestamp()
end = datetime.now().timestamp()



