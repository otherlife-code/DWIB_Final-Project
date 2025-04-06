# 🌀 ETL dan Pemeriksaan Kualitas Data dengan Apache Airflow

## 🎯 Tujuan  
Mengubah pipeline ETL berbasis DuckDB menjadi alur kerja terorkestrasi menggunakan **Apache Airflow**, serta menambahkan proses validasi kualitas data yang terotomasi. Proyek ini mempersiapkan data agar siap digunakan untuk **analisis**, **visualisasi**, dan **pemantauan kualitas data** harian.

---

## 🧱 Bagian 1: Menyiapkan Lingkungan Airflow

- Lingkungan dijalankan secara lokal menggunakan **Docker Compose**
- Koneksi ke sumber data berupa file CSV dari Google Drive
- **DuckDB** digunakan sebagai sistem data warehouse lokal

---

## 🛠️ Bagian 2: Desain dan Implementasi DAG

### 2.1 DAG Pipeline ETL

- Konversi pipeline Python ke dalam DAG menggunakan **TaskFlow API**
- Komponen utama DAG:
  - 🔄 **Ekstraksi** dari link Google Drive
  - 🧪 **Transformasi** menjadi tabel fakta dan dimensi
  - 📥 **Loading** ke DuckDB
  - 👀 Sensor memeriksa ketersediaan file

### 2.2 Fitur Airflow Lanjutan

- ❌ **Error Handling** dan **Retry** otomatis
- 📧 Notifikasi email untuk task gagal dan task sukses

### 2.3 Strategi Penjadwalan

- Jadwal eksekusi menggunakan `@daily`
- `catchup=False` digunakan agar DAG tidak menumpuk backlog
- Dokumentasi penjadwalan disediakan dalam dokumen terpisah

---

## 🧪 Bagian 3: Pengujian dan Dokumentasi

### 3.1 Pengujian DAG

- Eksekusi DAG dilakukan secara manual melalui UI Airflow
- Semua log task terekam dan diverifikasi

### 3.2 Dokumentasi

Disediakan dokumentasi berikut:

- 🗺 Diagram dependensi tugas DAG
- 📌 Tujuan dan deskripsi masing-masing task
- 🕒 Penjadwalan dan pemicu DAG
- 👁️‍🗨️ Pengaturan pemantauan dan email alert
- 🔁 Prosedur penanganan task failure

---

## 📐 Bagian 4: Kualitas Data

- DAG `dag_data_quality` dibuat secara terpisah
- Pemeriksaan kualitas mencakup:
  - ✅ Unik-nya `customer_key` di `dim_customer`
  - ✅ Null ratio di kolom `fact_transactions` tidak melebihi 10%
- Hasil validasi dicatat dalam `log_data_quality.csv`
- Notifikasi email dikirim berdasarkan hasil pemeriksaan

---

## 📦 Deliverable

### 🗂 Repositori Kode

- `dags/etl_duckdb_dag.py`
- `dags/etl_pipeline.py`
- `dags/dag_data_quality.py`

### 📚 Dokumentasi

- Dokumen strategi penjadwalan
- Dokumen metrik kualitas data

### 🧾 Bukti Eksekusi

- 📸 Tangkapan layar DAG sukses
- 📄 Log keberhasilan dan kegagalan
- 📸 Screenshot UI Airflow

---

## 📊 Kesiapan Visualisasi Data

Data telah ditransformasikan menjadi tabel-tabel dimensi dan fakta:

- Tabel dimensi: `dim_customer`, `dim_card`, `dim_time`, `dim_demographics`
- Tabel fakta: `fact_transactions`

Tabel siap digunakan untuk visualisasi seperti:

```sql
SELECT c.Attrition_Flag, AVG(f.Total_Trans_Amt) AS avg_amount
FROM fact_transactions f
JOIN dim_customer c ON f.customer_key = c.customer_key
GROUP BY c.Attrition_Flag;
