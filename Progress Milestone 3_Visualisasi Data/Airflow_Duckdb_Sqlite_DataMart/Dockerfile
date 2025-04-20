# Gunakan image resmi Airflow sebagai base
FROM apache/airflow:2.7.2-python3.10

# Switch ke user root untuk install tools tambahan
USER root

# Install SQLite CLI (opsional, hanya kalau kamu mau debugging manual)
RUN apt-get update && apt-get install -y sqlite3 && apt-get clean

# Kembali ke user airflow
USER airflow

# Copy file requirements
COPY requirements.txt .

# Install library Python yang dibutuhkan untuk DuckDB dan SQLite
RUN pip install --no-cache-dir -r requirements.txt
