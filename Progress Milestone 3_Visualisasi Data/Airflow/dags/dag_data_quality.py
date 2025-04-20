from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.utils.email import send_email
from airflow.utils.trigger_rule import TriggerRule
from datetime import timedelta
import duckdb
import pandas as pd
import os

DB_PATH = "/opt/airflow/dags/database.duckdb"
CSV_LOG_PATH = "/opt/airflow/dags/log_data_quality.csv"

@dag(
    dag_id="dag_data_quality",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
    tags=["data_quality"],
    default_args={
        'owner': 'julio',
        'retries': 1,
        'retry_delay': timedelta(minutes=3),
        'email': [
            'laurenziusjulioanreaja@mail.ugm.ac.id',
            'selvianisacahyamukti@mail.ugm.ac.id',
            'yudypratamafanggidae@mail.ugm.ac.id'
        ],
        'email_on_failure': True,
        'email_on_retry': False
    }
)
def data_quality_duckdb():

    @task()
    def check_null_ratio():
        conn = duckdb.connect(DB_PATH, read_only=True)
        df = conn.execute("SELECT * FROM fact_transactions").fetchdf()
        conn.close()

        null_ratio = df.isnull().mean()
        threshold = 0.10
        bad_columns = null_ratio[null_ratio > threshold]

        if not bad_columns.empty:
            raise ValueError(f"❌ Kolom dengan null >10%: {bad_columns.to_dict()}")

        return f"✅ Null ratio semua kolom OK: max {null_ratio.max():.2%}"

    @task()
    def check_customer_key_duplicate():
        conn = duckdb.connect(DB_PATH, read_only=True)
        dup_count = conn.execute("""
            SELECT COUNT(*) FROM (
                SELECT customer_key FROM dim_customer
                GROUP BY customer_key
                HAVING COUNT(*) > 1
            )
        """).fetchone()[0]
        conn.close()

        if dup_count > 0:
            raise ValueError(f"❌ Ditemukan {dup_count} customer_key yang duplikat!")
        return f"✅ customer_key OK, tidak ada duplikat"

    @task(trigger_rule=TriggerRule.ALL_DONE)
    def record_quality_log(null_check_msg: str, cust_check_msg: str):
        try:
            conn = duckdb.connect(DB_PATH, read_only=True)
            df = conn.execute("SELECT * FROM fact_transactions").fetchdf()
            total_rows = len(df)
            max_null = df.isnull().mean().max()

            dup_cust = conn.execute("""
                SELECT COUNT(*) FROM (
                    SELECT customer_key FROM dim_customer
                    GROUP BY customer_key
                    HAVING COUNT(*) > 1
                )
            """).fetchone()[0]
        except:
            total_rows = None
            max_null = None
            dup_cust = None

        null_ok = null_check_msg is not None and "✅" in null_check_msg
        cust_ok = cust_check_msg is not None and "✅" in cust_check_msg

        status = "success" if null_ok and cust_ok else "failed"
        notes = f"{null_check_msg or '❌'} | {cust_check_msg or '❌'}"

        log_entry = pd.DataFrame([{
            "run_date": pd.Timestamp.now(),
            "status": status,
            "total_rows": total_rows,
            "max_null_ratio": max_null,
            "duplicate_customer_key": dup_cust,
            "notes": notes
        }])

        if os.path.exists(CSV_LOG_PATH):
            log_entry.to_csv(CSV_LOG_PATH, mode='a', header=False, index=False)
        else:
            log_entry.to_csv(CSV_LOG_PATH, mode='w', header=True, index=False)

    @task(trigger_rule=TriggerRule.ALL_SUCCESS)
    def notify_passed():
        send_email(
            to=[
                'laurenziusjulioanreaja@mail.ugm.ac.id',
                'selvianisacahyamukti@mail.ugm.ac.id',
                'yudypratamafanggidae@mail.ugm.ac.id'
            ],
            subject="✅ Kualitas Data Lolos - dag_data_quality",
            html_content="""
            <h3>🎯 Pemeriksaan Kualitas Data Lolos</h3>
            <p>Tabel <strong>fact_transactions</strong> valid:</p>
            <ul>
                <li>customer_key di dim_customer tidak duplikat</li>
                <li>Semua kolom memiliki null &le; 10%</li>
            </ul>
            """
        )

    @task(trigger_rule=TriggerRule.ONE_FAILED)
    def notify_failed():
        send_email(
            to=[
                'laurenziusjulioanreaja@mail.ugm.ac.id',
                'selvianisacahyamukti@mail.ugm.ac.id',
                'yudypratamafanggidae@mail.ugm.ac.id'
            ],
            subject="❌ Kualitas Data Gagal - dag_data_quality",
            html_content="""
            <h3>⚠️ Pemeriksaan Kualitas Data GAGAL</h3>
            <p>Satu atau lebih metrik kualitas data tidak lolos ambang batas:</p>
            <ul>
                <li>Duplikat pada customer_key</li>
                <li>Rasio null kolom > 10%</li>
            </ul>
            <p>Silakan periksa log task Airflow untuk detail kesalahan.</p>
            """
        )

    t1 = check_null_ratio()
    t2 = check_customer_key_duplicate()
    log = record_quality_log(t1, t2)
    success = notify_passed()
    fail = notify_failed()

    [t1, t2] >> log >> [success, fail]

data_quality_duckdb()
