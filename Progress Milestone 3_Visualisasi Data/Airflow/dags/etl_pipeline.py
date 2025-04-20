import duckdb
import pandas as pd
import os
import urllib.request
from datetime import datetime

class ETLPipeline:
    def __init__(self, db_path, sharing_link=None, local_file_path="data.csv"):
        self.sharing_link = sharing_link
        self.db_path = db_path
        self.local_file_path = local_file_path
        self.conn = duckdb.connect(database=self.db_path)

    def initialize_warehouse(self):
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_customer (
            customer_key INT,
            CLIENTNUM INT,
            Attrition_Flag VARCHAR,
            Customer_Age INT,
            Months_on_book INT,
            Start_Date TIMESTAMP,
            End_Date TIMESTAMP,
            Is_Current BOOLEAN
        );
        """)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_card (
            Card_Key INT,
            Card_Category VARCHAR
        );
        """)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_demographics (
            demographic_key INT,
            Demographic_ID INT,
            Gender VARCHAR,
            Dependent_count INT,
            Education_Level VARCHAR,
            Marital_Status VARCHAR,
            Income_Category VARCHAR,
            Start_Date TIMESTAMP,
            End_Date TIMESTAMP,
            Is_Current BOOLEAN
        );
        """)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS dim_time (
            Time_Key INT,
            Months_Inactive_12_mon INT,
            Contacts_Count_12_mon INT
        );
        """)
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS fact_transactions (
            Transaction_ID INT,
            customer_key INT,
            Card_Key INT,
            demographic_key INT,
            Time_Key INT,
            Credit_Limit DOUBLE,
            Total_Revolving_Bal INT,
            Avg_Open_To_Buy DOUBLE,
            Total_Amt_Chng_Q4_Q1 DOUBLE,
            Total_Trans_Amt INT,
            Total_Trans_Ct INT,
            Total_Ct_Chng_Q4_Q1 DOUBLE,
            Avg_Utilization_Ratio DOUBLE
        );
        """)
        print("✅ Struktur data warehouse berhasil diinisialisasi.")

    def extract(self):
        if self.sharing_link:
            try:
                file_id = self.sharing_link.split('/d/')[1].split('/')[0]
                direct_download_link = f"https://drive.google.com/uc?export=download&id={file_id}"
                if not os.path.exists(self.local_file_path):
                    print("🔽 Mengunduh file dari Google Drive...")
                    urllib.request.urlretrieve(direct_download_link, self.local_file_path)
                    print(f"✅ File berhasil diunduh ke: {self.local_file_path}")
                else:
                    print(f"📂 Menggunakan file lokal: {self.local_file_path}")
            except Exception as e:
                raise RuntimeError(f"❌ Gagal mengunduh file dari Google Drive: {e}")

        try:
            df = pd.read_csv(self.local_file_path)
            print("✅ Data berhasil diekstrak.")
            return df
        except Exception as e:
            raise RuntimeError(f"❌ Gagal membaca file CSV: {e}")

    def transform(self, df):
        df = df.drop(columns=[
            'Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1',
            'Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2'
        ], errors='ignore')

        dim_customer = df[['CLIENTNUM', 'Attrition_Flag', 'Customer_Age', 'Months_on_book']].drop_duplicates().reset_index(drop=True)
        dim_customer['customer_key'] = dim_customer['CLIENTNUM']
        dim_customer['Start_Date'] = '2022-01-01'
        dim_customer['End_Date'] = None
        dim_customer['Is_Current'] = True
        dim_customer = dim_customer[[
            'customer_key', 'CLIENTNUM', 'Attrition_Flag', 'Customer_Age', 'Months_on_book',
            'Start_Date', 'End_Date', 'Is_Current'
        ]]

        dim_card = df[['Card_Category']].drop_duplicates().reset_index(drop=True)
        dim_card['Card_Key'] = range(1, len(dim_card) + 1)
        dim_card = dim_card[['Card_Key', 'Card_Category']]

        dim_time = df[['Months_Inactive_12_mon', 'Contacts_Count_12_mon']].drop_duplicates().reset_index(drop=True)
        dim_time['Time_Key'] = range(1, len(dim_time) + 1)
        dim_time = dim_time[['Time_Key', 'Months_Inactive_12_mon', 'Contacts_Count_12_mon']]

        dim_demographics = df[['Gender', 'Dependent_count', 'Education_Level', 'Marital_Status', 'Income_Category']].drop_duplicates().reset_index(drop=True)
        dim_demographics['demographic_key'] = dim_demographics.index + 1
        dim_demographics['Demographic_ID'] = dim_demographics['demographic_key']
        dim_demographics['Start_Date'] = '2022-01-01'
        dim_demographics['End_Date'] = None
        dim_demographics['Is_Current'] = True
        dim_demographics = dim_demographics[[
            'demographic_key', 'Demographic_ID', 'Gender', 'Dependent_count', 'Education_Level',
            'Marital_Status', 'Income_Category', 'Start_Date', 'End_Date', 'Is_Current'
        ]]

        fact_transactions = (
            df
            .merge(dim_customer, on=['CLIENTNUM', 'Attrition_Flag', 'Customer_Age', 'Months_on_book'], how='left')
            .merge(dim_card, on=['Card_Category'], how='left')
            .merge(dim_demographics, on=['Gender', 'Dependent_count', 'Education_Level', 'Marital_Status', 'Income_Category'], how='left')
            .merge(dim_time, on=['Months_Inactive_12_mon', 'Contacts_Count_12_mon'], how='left')
        )

        fact_transactions = fact_transactions[[
            'customer_key', 'Card_Key', 'demographic_key', 'Time_Key',
            'Credit_Limit', 'Total_Revolving_Bal', 'Avg_Open_To_Buy',
            'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct',
            'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio'
        ]].reset_index(drop=True)

        fact_transactions['Transaction_ID'] = range(1, len(fact_transactions) + 1)

        fact_transactions = fact_transactions[[
            'Transaction_ID', 'customer_key', 'Card_Key', 'demographic_key', 'Time_Key',
            'Credit_Limit', 'Total_Revolving_Bal', 'Avg_Open_To_Buy',
            'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct',
            'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio'
        ]]

        return dim_customer, dim_card, dim_demographics, dim_time, fact_transactions

    def load(self, dim_customer, dim_card, dim_demographics, dim_time, fact_transactions):
        self.load_from_pandas(dim_customer, dim_card, dim_demographics, dim_time, fact_transactions)

    def load_from_pandas(self, dim_customer, dim_card, dim_demographics, dim_time, fact_transactions):
        self.conn.execute("DELETE FROM dim_customer")
        self.conn.register('df_dim_customer', dim_customer)
        self.conn.execute("INSERT INTO dim_customer SELECT * FROM df_dim_customer")

        self.conn.execute("DELETE FROM dim_card")
        self.conn.register('df_dim_card', dim_card)
        self.conn.execute("INSERT INTO dim_card SELECT * FROM df_dim_card")

        self.conn.execute("DELETE FROM dim_demographics")
        self.conn.register('df_dim_demographics', dim_demographics)
        self.conn.execute("INSERT INTO dim_demographics SELECT * FROM df_dim_demographics")

        self.conn.execute("DELETE FROM dim_time")
        self.conn.register('df_dim_time', dim_time)
        self.conn.execute("INSERT INTO dim_time SELECT * FROM df_dim_time")

        self.conn.register('df_fact_transactions', fact_transactions)
        self.conn.execute("CREATE OR REPLACE TABLE temp_fact_transactions AS SELECT * FROM df_fact_transactions")

        self.conn.execute("""
        INSERT INTO fact_transactions
        SELECT
            f.Transaction_ID,
            c.customer_key,
            cr.Card_Key,
            d.demographic_key,
            t.Time_Key,
            f.Credit_Limit,
            f.Total_Revolving_Bal,
            f.Avg_Open_To_Buy,
            f.Total_Amt_Chng_Q4_Q1,
            f.Total_Trans_Amt,
            f.Total_Trans_Ct,
            f.Total_Ct_Chng_Q4_Q1,
            f.Avg_Utilization_Ratio
        FROM temp_fact_transactions f
        JOIN dim_customer c ON f.customer_key = c.customer_key
        JOIN dim_card cr ON f.Card_Key = cr.Card_Key
        JOIN dim_demographics d ON f.demographic_key = d.demographic_key
        JOIN dim_time t ON f.Time_Key = t.Time_Key
        """)

        self.conn.execute("DROP TABLE temp_fact_transactions")
        print("✅ Data berhasil dimuat ke data warehouse.")

    def __del__(self):
        try:
            if hasattr(self, 'conn'):
                self.conn.close()
                print("🔌 Koneksi DuckDB ditutup.")
        except:
            pass
