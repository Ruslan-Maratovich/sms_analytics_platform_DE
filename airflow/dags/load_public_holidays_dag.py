from airflow import DAG

from airflow.operators.bash import BashOperator

from datetime import datetime


with DAG(
    dag_id="load_public_holidays",
    start_date=datetime(2026,1,1),
    schedule="0 2 1 * *",
    catchup=False,
    tags=[
        "sms",
        "api",
        "clickhouse"
    ]
) as dag:


    load_holidays = BashOperator(

        task_id="load_nager_holidays",

        bash_command=
        """
        python /opt/airflow/scripts/load_public_holidays.py
        """

    )
    load_holidays