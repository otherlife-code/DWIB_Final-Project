from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import duckdb
import sqlite3
import pandas as pd

DUCKDB_PATH = '/opt/airflow/data/database.duckdb'
SQLITE_PATH = '/opt/airflow/data/database_baru.sqlite'

def migrate_duckdb_to_sqlite():
    # 1. Koneksi ke DuckDB
    con_duck = duckdb.connect(DUCKDB_PATH)
    
    # 2. Koneksi ke SQLite
    con_sqlite = sqlite3.connect(SQLITE_PATH)
    
    # 3. Ambil semua nama tabel
    tables = con_duck.execute("SHOW TABLES").fetchall()
    tables = [t[0] for t in tables]
    
    # 4. Migrasi tiap tabel
    for table in tables:
        print(f"Memigrasikan tabel: {table}")
        df = con_duck.execute(f"SELECT * FROM {table}").df()
        df.to_sql(table, con_sqlite, if_exists='replace', index=False)

    # 5. Tutup koneksi
    con_duck.close()
    con_sqlite.close()
    print("✅ Migrasi selesai!")

# Definisikan DAG
with DAG(
    dag_id='migrate_duckdb_to_sqlite',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['duckdb', 'sqlite', 'migration']
) as dag:

    migrate_task = PythonOperator(
        task_id='migrate_all_tables',
        python_callable=migrate_duckdb_to_sqlite
    )

    migrate_task
