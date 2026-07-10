from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime


def hello():
    print("hello from Airflow worker!")


with DAG(
    dag_id = "hello_world",
    start_date = datetime(2026, 7, 9),
    schedule = "@daily",
    catchup = False,
) as dag:

    task = PythonOperator(
        task_id = "hello_task",
        python_callable = hello
    )

    task