from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="contoh_dag_pertamaku",
    start_date=datetime(2024, 3, 21),
    schedule_interval="@daily",
    catchup=False
) as dag:
    task_1 = BashOperator(
        task_id='hello_task',
        bash_command='echo Hello Airflow dari Julio!'
    )
