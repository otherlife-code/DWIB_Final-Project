from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from datetime import timedelta
from airflow.utils.email import send_email
from airflow.utils.trigger_rule import TriggerRule
from etl_pipeline import ETLPipeline
import os
import pandas as pd

DB_PATH = "/opt/airflow/dags/database.duckdb"
DATA_PATH = "/opt/airflow/dags/data.csv"
GDRIVE_LINK = "https://drive.google.com/file/d/1Ii-ZwI4v9ja1kC21HqygyhMqgAEpS1mo/view?usp=sharing"

@dag(
    dag_id="etl_duckdb_dag_custom_class",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    tags=["ETL", "duckdb"],
    default_args={
        'owner': 'julio',
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        'email': [
            'laurenziusjulioanreaja@mail.ugm.ac.id',
            'selvianisacahyamukti@mail.ugm.ac.id',
            'yudypratamafanggidae@mail.ugm.ac.id'
        ],
        'email_on_failure': True,
        'email_on_retry': False
    }
)
def etl_duckdb_custom():

    @task()
    def check_data():
        return os.path.exists(DATA_PATH)

    @task()
    def init():
        pipeline = ETLPipeline(DB_PATH, GDRIVE_LINK, DATA_PATH)
        pipeline.initialize_warehouse()

    @task()
    def extract():
        pipeline = ETLPipeline(DB_PATH, GDRIVE_LINK, DATA_PATH)
        df = pipeline.extract()
        return df.to_json(orient="split")

    @task()
    def transform(df_json):
        df = pd.read_json(df_json, orient="split")
        pipeline = ETLPipeline(DB_PATH, GDRIVE_LINK, DATA_PATH)
        dim_customer, dim_card, dim_demographics, dim_time, fact_transactions = pipeline.transform(df)
        return {
            "dim_customer": dim_customer.to_json(orient="split"),
            "dim_card": dim_card.to_json(orient="split"),
            "dim_demographics": dim_demographics.to_json(orient="split"),
            "dim_time": dim_time.to_json(orient="split"),
            "fact_transactions": fact_transactions.to_json(orient="split"),
        }

    @task()
    def load(dfs):
        pipeline = ETLPipeline(DB_PATH, GDRIVE_LINK, DATA_PATH)
        pipeline.load(
            pd.read_json(dfs["dim_customer"], orient="split"),
            pd.read_json(dfs["dim_card"], orient="split"),
            pd.read_json(dfs["dim_demographics"], orient="split"),
            pd.read_json(dfs["dim_time"], orient="split"),
            pd.read_json(dfs["fact_transactions"], orient="split")
        )
        return {
            "num_records": len(pd.read_json(dfs["fact_transactions"], orient="split")),
            "timestamp": pd.Timestamp.now().isoformat()
        }

    @task(trigger_rule=TriggerRule.ALL_SUCCESS)
    def notify_success(info: dict):
        send_email(
            to=[
                'laurenziusjulioanreaja@mail.ugm.ac.id',
                'selvianisacahyamukti@mail.ugm.ac.id',
                'yudypratamafanggidae@mail.ugm.ac.id'
            ],
            subject='✅ ETL Sukses - etl_duckdb_dag_custom_class',
            html_content=f"""
            <h3>🎉 Proses ETL Sukses</h3>
            <p>DAG: <strong>etl_duckdb_dag_custom_class</strong></p>
            <p>Jumlah transaksi dimuat: <strong>{info.get("num_records", "?" )}</strong></p>
            <p>Waktu: <strong>{info.get("timestamp", "?" )}</strong></p>
            """
        )

    @task(trigger_rule=TriggerRule.ONE_FAILED)
    def notify_failure():
        send_email(
            to=[
                'laurenziusjulioanreaja@mail.ugm.ac.id',
                'selvianisacahyamukti@mail.ugm.ac.id',
                'yudypratamafanggidae@mail.ugm.ac.id'
            ],
            subject='❌ ETL Gagal - etl_duckdb_dag_custom_class',
            html_content="""
            <h3>⚠️ ETL Pipeline Gagal</h3>
            <p>Salah satu task gagal dalam proses DAG <strong>etl_duckdb_dag_custom_class</strong>.</p>
            <p>Silakan cek log di Airflow UI untuk detail.</p>
            """
        )

    # DAG chain
    file_ready = check_data()
    db_ready = init()
    df_raw = extract()
    df_transformed = transform(df_raw)
    etl_result = load(df_transformed)
    success = notify_success(etl_result)
    fail = notify_failure()

    file_ready >> db_ready >> df_raw >> df_transformed >> etl_result
    etl_result >> [success, fail]

etl_duckdb_custom()
