from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sqlite3

SQLITE_PATH = '/opt/airflow/data/database_baru.sqlite'

def create_sqlite_data_marts_and_views():
    conn = sqlite3.connect(SQLITE_PATH)

    # Drop views dan tabel jika sudah ada
    conn.execute("DROP VIEW IF EXISTS v_avg_utilization_by_card_sqlite;")
    conn.execute("DROP VIEW IF EXISTS v_total_trans_by_income_sqlite;")
    conn.execute("DROP VIEW IF EXISTS v_avg_contacts_by_attrition_sqlite;")
    conn.execute("DROP VIEW IF EXISTS v_trans_by_customer_status_sqlite;")
    conn.execute("DROP VIEW IF EXISTS v_kpi_churn_retention_sqlite;")
    conn.execute("DROP VIEW IF EXISTS v_customer_ltv_sqlite;")
    conn.execute("DROP TABLE IF EXISTS dm_analysis_sqlite;")
    conn.execute("DROP TABLE IF EXISTS dm_operational_sqlite;")
    conn.commit()

    # Data Mart: dm_analysis_sqlite
    conn.execute("""
    CREATE TABLE dm_analysis_sqlite AS
    SELECT 
      f.Transaction_ID,
      f.Credit_Limit,
      f.Total_Trans_Amt,
      f.Total_Trans_Ct,
      f.Total_Revolving_Bal,
      f.Avg_Utilization_Ratio,
      t.Months_Inactive_12_mon,
      t.Contacts_Count_12_mon,
      c.Customer_Age,
      c.Months_on_book,
      d.Card_Category,
      g.Gender,
      g.Education_Level,
      g.Income_Category,
      c.Attrition_Flag
    FROM fact_transactions f
    JOIN dim_time t ON f.Time_Key = t.Time_Key
    JOIN dim_customer c ON f.customer_key = c.Customer_Key
    JOIN dim_card d ON f.Card_Key = d.Card_Key
    JOIN dim_demographics g ON f.demographic_key = g.demographic_key;
    """)

    # View 1
    conn.execute("""
    CREATE VIEW v_avg_utilization_by_card_sqlite AS
    SELECT 
      Card_Category,
      AVG(Avg_Utilization_Ratio) AS avg_util_ratio
    FROM dm_analysis_sqlite
    GROUP BY Card_Category;
    """)

    # View 2
    conn.execute("""
    CREATE VIEW v_total_trans_by_income_sqlite AS
    SELECT 
      Income_Category,
      SUM(Total_Trans_Amt) AS total_transaction
    FROM dm_analysis_sqlite
    GROUP BY Income_Category;
    """)

    # Data Mart: dm_operational_sqlite
    conn.execute("""
    CREATE TABLE dm_operational_sqlite AS
    SELECT 
      f.Transaction_ID,
      f.Time_Key,
      f.Customer_Key,
      f.Total_Trans_Ct,
      f.Total_Trans_Amt,
      f.Avg_Open_To_Buy,
      c.Attrition_Flag,
      t.Months_Inactive_12_mon,
      t.Contacts_Count_12_mon
    FROM fact_transactions f
    JOIN dim_customer c ON f.customer_key = c.Customer_Key
    JOIN dim_time t ON f.Time_Key = t.Time_Key;
    """)

    # View 3
    conn.execute("""
    CREATE VIEW v_avg_contacts_by_attrition_sqlite AS
    SELECT 
      Attrition_Flag,
      AVG(Contacts_Count_12_mon) AS avg_contacts
    FROM dm_operational_sqlite
    GROUP BY Attrition_Flag;
    """)

    # View 4
    conn.execute("""
    CREATE VIEW v_trans_by_customer_status_sqlite AS
    SELECT 
      Attrition_Flag,
      AVG(Total_Trans_Ct) AS avg_transactions
    FROM dm_operational_sqlite
    GROUP BY Attrition_Flag;
    """)

    # View 5: KPI churn dan retention (TOTAL tanpa waktu)
    conn.execute("""
    CREATE VIEW v_kpi_churn_retention_sqlite AS
    SELECT 
      'TOTAL' AS period,
      COUNT(DISTINCT customer_key) AS total_customers,
      SUM(CASE WHEN Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) AS churned_customers,
      ROUND(SUM(CASE WHEN Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) * 1.0 
            / COUNT(DISTINCT customer_key), 4) AS churn_rate,
      ROUND(1 - (SUM(CASE WHEN Attrition_Flag = 'Attrited Customer' THEN 1 ELSE 0 END) * 1.0 
            / COUNT(DISTINCT customer_key)), 4) AS retention_rate
    FROM dm_operational_sqlite;
    """)

    # View 6: Estimasi CLV
    conn.execute("""
    CREATE VIEW v_customer_ltv_sqlite AS
    SELECT 
      Customer_Key,
      Customer_Age,
      Months_on_book,
      SUM(Total_Trans_Amt) AS total_spending,
      AVG(Total_Trans_Amt) AS avg_spending_per_tx,
      COUNT(Transaction_ID) AS total_tx,
      ROUND(SUM(Total_Trans_Amt) * 1.0 / NULLIF(Months_on_book, 0), 2) AS monthly_value,
      ROUND(SUM(Total_Trans_Amt) * 0.75, 2) AS estimated_clv
    FROM dm_analysis_sqlite
    GROUP BY 
      customer_key, Customer_Age, Months_on_book;
    """)

    conn.commit()
    conn.close()
    print("✅ Data mart dan view di SQLite berhasil dibuat tanpa kolom transaction_date.")

# DAG definition
with DAG(
    dag_id='dag_sqlite_data_mart',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=['sqlite', 'datamart', 'kpi']
) as dag:

    task_create_sqlite_dm = PythonOperator(
        task_id='sqlite_dm_and_views',
        python_callable=create_sqlite_data_marts_and_views
    )

    task_create_sqlite_dm
