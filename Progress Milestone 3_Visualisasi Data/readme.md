# Bank Churners Project - Data Warehouse & Dashboard

## ✨ Deskripsi Proyek

Proyek ini merupakan implementasi lengkap dari proses perancangan *Data Warehouse*, pembangunan *Data Mart* di DuckDB/SQLite, hingga visualisasi data interaktif melalui dashboard Metabase, berdasarkan dataset pelanggan kartu kredit (Bank Churners).

---

## 📂 1. Persiapan Data dan Data Mart (25%)

### Data Mart 1: `dm_analysis`
- Fokus: Analisis historis dan tren pelanggan
- Struktur: Tabel terpisah berisi gabungan fakta dan dimensi pelanggan
- Dimensi yang digunakan:
  - `dim_customer`
  - `dim_card`
  - `dim_demographics`
  - `dim_time`
  - `fact_transactions`

### Data Mart 2: `dm_operational`
- Fokus: Metrik operasional & metrik analisis
- Dimensi yang digunakan: transaksi, waktu, status pelanggan

### View yang Dibuat:
- `v_avg_utilization_by_card_sqlite`
- `v_total_trans_by_income_sqlite`
- `v_avg_contacts_by_attrition_sqlite`
- `v_trans_by_customer_status_sqlite`
- `v_kpi_churn_retention_sqlite`
- `v_customer_ltv_sqlite`



## 💡 2. Pemilihan dan Setup Alat Visualisasi (10%)

### Alat yang Dipilih: **Metabase**

### Alasan:
- Open source dan ringan untuk deployment
- Mendukung SQLite, PostgreSQL, dan banyak sumber lainnya
- Fitur bawaan lengkap: filter, tooltip, drill-down, pivot table
- Integrasi mudah dengan Docker dan Airflow

### Langkah Setup:
- Deploy menggunakan `docker-compose.yaml`
- Tambahkan koneksi database dan postgresql
- Cek integrasi dengan folder `/data/database_baru.sqlite`


## 🎨 3. Desain Dashboard (35%)

### Nama Dashboard: `Customer Retention Insight`

![dashboard](./data/dashboard_preview.png)

### Visualisasi Utama:
1. **KPI Cards**
   - Total Customer
   - Churn Rate
   - Average CLV
   - Retention Rate
2. **Pie Chart** - Transaksi berdasarkan segmen pendapatan
3. **Bar Chart** - Rata-rata utilisasi per kategori kartu
4. **Scatter Plot** - Distribusi CLV berdasarkan status pelanggan

### Filter Interaktif:
- Filter `Card_Category` (kategori kartu)
- Filter `Income_Category` (kategori pendapatan)

### Pertanyaan Bisnis yang Dijawab:
- Siapa pelanggan bernilai tinggi (CLV tertinggi)?
- Apakah pelanggan churn memiliki pola aktivitas berbeda?
- Kategori kartu atau pendapatan mana yang cenderung churn lebih tinggi?

---

## 📊 4. Visualisasi Interaktif (20%)

### Fitur Interaktif:
- **Filtering Global** untuk semua chart melalui parameter Metabase
- **Hover Tooltips** aktif di semua visualisasi
- **Drill Down** tersedia untuk setiap tabel dan chart (View Data)

---
