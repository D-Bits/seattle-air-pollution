from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime


default_args = {
    "owner": "airflow",
    "start_date": datetime(2020, 11, 1),
    "retries": 1,
}

dag = DAG(
    "db_init", 
    schedule_interval=None, 
    template_searchpath=['/usr/local/airflow/dags/sql'], 
    catchup=False, 
    default_args=default_args
)

with dag:

    t1 = PostgresOperator(
        task_id="create_db", 
        sql="CREATE DATABASE pollution;", 
        postgres_conn_id="postgres_main", 
        autocommit=True
    )

    t2 = PostgresOperator(
        task_id="create_tables",
        sql="tables.sql",
        postgres_conn_id="postgres_main",
        database="pollution",
        autocommit=True
    )

    t1 >> t2
