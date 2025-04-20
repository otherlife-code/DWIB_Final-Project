from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import duckdb
import os

def query_duckdb():
    # Path absolut dalam container Docker (pastikan volume ./data sudah dimount ke /opt/airflow/data)
    db_path = '/opt/airflow/data/database.duckdb'

    try:
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"File tidak ditemukan: {db_path}")

        conn = duckdb.connect(db_path)

        # Cek apakah tabel dim_time ada
        tables = [t[0] for t in conn.execute("SHOW TABLES").fetchall()]
        print("Tabel tersedia:", tables)

        if "dim_time" not in tables:
            raise Exception("Tabel 'dim_time' tidak ditemukan di dalam database.")

        result = conn.execute("SELECT * FROM dim_time LIMIT 5").fetchall()
        print("Data dari DuckDB (tabel `dim_time`):")
        for row in result:
            print(row)

        conn.close()
    except Exception as e:
        print("Gagal menjalankan query ke DuckDB:", e)

with DAG(
    dag_id='etl_duckdb',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['duckdb'],
) as dag:

    query_task = PythonOperator(
        task_id='query_duckdb',
        python_callable=query_duckdb
    )
