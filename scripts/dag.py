from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.docker_operator import DockerOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False}

DAG =DAG(
    'docker_dag',
    default_args=default_args,
    description='A simple Docker DAG',
    start_date=datetime(2024, 02, 20))

