# Bank Churners Project - Data Warehouse & Dashboard

## ✨ Deskripsi Proyek

Proyek ini merupakan implementasi lengkap dari proses perancangan *Data Warehouse*, pembangunan *Data Mart* di DuckDB/SQLite, hingga visualisasi data interaktif melalui dashboard Metabase, berdasarkan dataset pelanggan kartu kredit (Bank Churners).

- Link Dashboard = https://bankchurnerss.metabaseapp.com/public/dashboard/b68f0e4e-84a7-4c28-992a-f4a531c85c79?card_category=&income_category=&teks=
- Link Video     = 
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

![Dashboard Preview](https://github.com/otherlife-code/DWIB_Final-Project/raw/main/Progress%20Milestone%203_Visualisasi%20Data/Asset/Dashboard_1.png)
![Dashboard Preview_2](https://github.com/otherlife-code/DWIB_Final-Project/blob/main/Progress%20Milestone%203_Visualisasi%20Data/Asset/Dashboard_2.png)

### Visualisasi Utama:
1. **KPI Cards**
   - Total Customer
   - Churn Rate
   - Average CLV
   - Retention Rate
2. **Pie Chart** - Transaksi berdasarkan segmen pendapatan
3. **Bar Chart** - Rata-rata utilisasi per kategori kartu
4. **Scatter Plot** - Distribusi CLV berdasarkan status pelanggan
5. **Sanskey Plot** - Korelasi Utilitas dan Inaktivitas Customer
6. **Tabel** - Top 10 Pelanggan dengan Customer Lifetime Value terbaik

### Filter Interaktif:
- Filter `Card_Category` (kategori kartu)
- Filter `Income_Category` (kategori pendapatan)

### Pertanyaan Bisnis yang Dijawab:
- Siapa pelanggan bernilai tinggi (CLV tertinggi)?
- Apakah pelanggan churn memiliki pola aktivitas berbeda?
- Kategori kartu atau pendapatan mana yang cenderung churn lebih tinggi?

## 1. Pelanggan Bernilai Tinggi (Top 10 CLV)

| Rank | Customer Key | Estimated CLV | Usia Pelanggan | Segment Pendapatan |
|-----:|-------------:|-------------:|---------------:|-------------------:|
| 1    | 2581         | 8 450.00     | 42             | $80K–$120K         |
| 2    | 4267         | 7 982.50     | 35             | $60K–$80K          |
| 3    | 3190         | 7 540.00     | 50             | > $120K            |
| 4    | 1123         | 7 425.00     | 29             | $40K–$60K          |
| 5    | 5894         | 7 120.00     | 47             | $80K–$120K         |
| 6    | 2047         | 6 985.00     | 53             | > $120K            |
| 7    | 3178         | 6 890.00     | 38             | $60K–$80K          |
| 8    | 4901         | 6 725.00     | 44             | $40K–$60K          |
| 9    | 1389         | 6 590.00     | 31             | $80K–$120K         |
| 10   | 7752         | 6 450.00     | 28             | $60K–$80K          |

> **Insight:** Pelanggan dengan `customer_key` seperti 2581, 4267, dan 3190 memiliki nilai seumur hidup (CLV) tertinggi dan menjadi prioritas bagi program retensi dan upsell.

---

## 2. Pola Aktivitas Churn vs Non-Churn

| Status Pelanggan   | Rata-rata Transaksi | Rata-rata Utilisasi | Rata-rata Kontak per Tahun |
|--------------------|---------------------:|--------------------:|----------------------------:|
| Existing Customer  | 45.12                | 0.523               | 2.87                        |
| Attrited Customer  | 35.47                | 0.462               | 5.13                        |

> **Insight:**  
> - Pelanggan yang churn melakukan **lebih banyak kontak** (5.13 vs 2.87) namun **menggunakan limit** dan **bertransaksi** lebih sedikit dibanding yang tetap.  
> - Artinya, kontak yang tinggi bisa menjadi sinyal peringatan dini churn.

---

## 3. Segmen Paling Rawan Churn

### 3a. Berdasarkan Kategori Kartu

| Kategori Kartu | Churn Rate |
|---------------:|-----------:|
| Silver         | 18.0 %     |
| Gold           | 15.2 %     |
| Platinum       | 12.0 %     |
| Blue           | 9.8 %      |

> **Insight:** Kartu **Silver** paling rawan churn (~18%), sementara **Blue** dan **Platinum** relatif lebih stabil.

### 3b. Berdasarkan Segmen Pendapatan

| Segment Pendapatan | Churn Rate |
|-------------------:|-----------:|
| < $40K             | 20.0 %     |
| $40K–$60K         | 14.5 %     |
| $60K–$80K         | 13.2 %     |
| > $80K             | 9.5 %      |

> **Insight:** Pelanggan berpendapatan **< $40K** memiliki risiko churn tertinggi (20 %), sedangkan pendapatan lebih tinggi cenderung lebih stabil.

---

Dengan tiga insight di atas, tim bisnis dapat:

1. **Memprioritaskan** top CLV customers untuk program loyalitas.  
2. **Menangani** pelanggan dengan pola kontak tinggi sebagai potensi churn.  
3. **Mengalokasikan** upaya retensi pada kategori kartu dan segmen pendapatan dengan churn tertinggi.  

---

## 📊 4. Visualisasi Interaktif (20%)

### Fitur Interaktif:
- **Filtering Global** untuk semua chart melalui parameter Metabase
- **Hover Tooltips** aktif di semua visualisasi
- **Drill Down** tersedia untuk setiap tabel dan chart (View Data)

---
