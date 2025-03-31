# 📊 Data Orchestration dengan Apache Airflow

## 🎯 Tujuan
Mengubah implementasi Data Warehouse DuckDB dan pipeline ETL dari tugas sebelumnya menjadi alur kerja yang siap produksi dan terorkestrasi menggunakan **Apache Airflow**. Tugas ini mempersiapkan pipeline data Anda untuk keperluan **visualisasi** dan **penggunaan operasional** lainnya.

---

## 🧱 Bagian 1: Menyiapkan Lingkungan Airflow

- Siapkan lingkungan Airflow lokal (menggunakan **Docker** atau instalasi langsung)
- Konfigurasikan koneksi yang diperlukan untuk **sumber data** dan **DuckDB**

---

## 🛠️ Bagian 2: Desain dan Implementasi DAG

### 2.1 DAG Pipeline ETL

Konversi pipeline ETL sebelumnya menjadi DAG di Airflow:

- Implementasikan dependensi tugas menggunakan:
  - Operator tradisional (`>>` dan `<<`), atau
  - TaskFlow API dengan `@task` decorators (opsional)
- Komponen DAG:
  - 🔄 **Ekstraksi** dari setiap sumber data
  - 🧪 **Transformasi** sesuai definisi ETL
  - 📥 **Loading** ke dalam data warehouse DuckDB
  - 👀 Setidaknya satu **Sensor** untuk cek ketersediaan data

### 2.2 Fitur Airflow Lanjutan

Implementasikan setidaknya **dua** fitur lanjutan berikut:

- 🔀 Branching logic berdasarkan kondisi
- ♻️ Dynamic task generation
- 🧩 Custom operators untuk logika bisnis tertentu
- ❌ Error handling dan mekanisme retry
- 📣 Notifikasi (Email/Slack) untuk status berhasil/gagal
- ⏱ SLA dan pemantauan
- ⏪ Backfilling capabilities

### 2.3 Strategi Penjadwalan dan Partisi

- Rancang strategi **penjadwalan** DAG yang sesuai
- Dokumentasikan keputusan penjadwalan dan **alasannya**

---

## 🧪 Bagian 3: Pengujian dan Dokumentasi

### 3.1 Pengujian DAG

- Uji DAG menggunakan fitur testing Airflow
- Sertakan log eksekusi yang berhasil

### 3.2 Dokumentasi

Dokumentasi wajib meliputi:

- 🗺 Diagram arsitektur DAG & dependensi
- 📌 Deskripsi tujuan setiap task
- 🕒 Informasi penjadwalan & dependensi
- 👁️‍🗨️ Pengaturan pemantauan & peringatan
- 🔁 Prosedur pemulihan kegagalan

---

## 📐 Bagian 4: Kualitas Data

- Implementasikan minimal **dua pemeriksaan kualitas data** menggunakan:
  - Airflow
  - Great Expectations
  - Python Native
- Buat DAG **terpisah** untuk memantau kualitas data
- Dokumentasikan:
  - Metrik kualitas data
  - Ambang batas (threshold)

---

## 📦 Deliverable

### 🗂 Repositori Kode
- File definisi DAG Airflow
- Script Python untuk ETL, sensor, dan validasi

### 📚 Dokumentasi
- Diagram arsitektur DAG
- Dokumen strategi penjadwalan
- Dokumen metrik kualitas data

### 🧾 Bukti Eksekusi
- 📸 Tangkapan layar DAG yang sukses dijalankan
- 📄 Log eksekusi yang valid
- 📸 Tampilan UI Airflow yang menampilkan DAG

---

## 📊 Rencana Persiapan Visualisasi

- Ringkasan kesiapan data untuk divisualisasikan
- Rekomendasi alat visualisasi:
  - Contoh: **Metabase**, **Apache Superset**, atau **Power BI**
- Contoh kueri yang berguna untuk visualisasi:
  ```sql
  SELECT customer_id, SUM(order_total) as total_spent
  FROM orders
  GROUP BY customer_id
  ORDER BY total_spent DESC
  LIMIT 10;

