from airflow.decorators import dag, task
from datetime import datetime


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 11, 1),
    "retries": 1,
}
