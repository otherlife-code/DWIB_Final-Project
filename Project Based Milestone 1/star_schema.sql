# Tabel Dimensi Pelanggan dengan dukungan SCD Type 2
conn.execute("""
CREATE OR REPLACE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    CLIENTNUM INT NOT NULL,
    Attrition_Flag VARCHAR,
    Customer_Age INT,
    Months_on_book INT,
    Start_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    End_Date TIMESTAMP,
    Is_Current BOOLEAN DEFAULT TRUE
);
""")

# Tabel Dimensi Kartu (statis)
conn.execute("""
CREATE OR REPLACE TABLE dim_card (
    Card_Key INT PRIMARY KEY,
    Card_Category VARCHAR
);
""")

# Tabel Dimensi Demografi dengan opsi untuk SCD Type 2
conn.execute("""
CREATE OR REPLACE TABLE dim_demographics (
    demographic_key INT PRIMARY KEY,
    Demographic_ID INT NOT NULL,
    Gender VARCHAR,
    Dependent_count INT,
    Education_Level VARCHAR,
    Marital_Status VARCHAR,
    Income_Category VARCHAR,
    Start_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    End_Date TIMESTAMP,
    Is_Current BOOLEAN DEFAULT TRUE
);
""")

# Tabel Dimensi Waktu (statis)
conn.execute("""
CREATE OR REPLACE TABLE dim_time (
    Time_Key INT PRIMARY KEY,
    Months_Inactive_12_mon INT,
    Contacts_Count_12_mon INT
);
""")

# Tabel Fakta Transaksi (mendukung ETL Inkremental)
conn.execute("""
CREATE OR REPLACE TABLE fact_transactions (
    Transaction_ID INT PRIMARY KEY,
    customer_key INT,
    Card_key INT,
    demographic_key INT,
    Time_Key INT,
    Credit_Limit DECIMAL(10,2),
    Total_Revolving_Bal INTEGER,
    Avg_Open_To_Buy DECIMAL(10,2),
    Total_Amt_Chng_Q4_Q1 DECIMAL(10,2),
    Total_Trans_Amt INTEGER,
    Total_Trans_Ct INTEGER,
    Total_Ct_Chng_Q4_Q1 DECIMAL(10,2),
    Avg_Utilization_Ratio DECIMAL(10,2),

    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
    FOREIGN KEY (Card_Key) REFERENCES dim_card(Card_Key),
    FOREIGN KEY (demographic_key) REFERENCES dim_demographics(demographic_key),
    FOREIGN KEY (Time_Key) REFERENCES dim_time(Time_Key)

);
""")

# Mengecek daftar tabel dalam database
print(conn.execute("SHOW TABLES;").fetchdf())