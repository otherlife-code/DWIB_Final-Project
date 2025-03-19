# Data Warehouse dan ETL Pipeline dengan DuckDB

## 📌 Tujuan
Mengimplementasikan data warehouse dan pipeline ETL menggunakan **DuckDB**, dengan fokus pada **pemodelan dimensi** dan **proses ETL** yang realistis untuk sebuah bisnis pilihan.

---

## 📂 Bagian 1: Data Modeling untuk Data Warehouse

### 1.1 Dokumen Kebutuhan Bisnis
- **Pilih domain bisnis** (Retail, Perbankan, Layanan Kesehatan, Pendidikan, e-Commerce, dll.)
- Buat dokumen kebutuhan bisnis yang mencakup:
  - Deskripsi bisnis
  - Tujuan analitis dan pertanyaan bisnis yang harus dijawab
  - Sumber data yang tersedia
  - Indikator utama (KPI) yang perlu dimonitor
  - Jenis laporan dan analisis yang dibutuhkan

### 1.2 Desain Skema Data Warehouse
- Buat **diagram skema** dengan DBDiagram.io atau Draw.io
- Implementasikan salah satu model:
  - **Star Schema**: Min. 1 tabel fakta & 4 tabel dimensi
  - **Snowflake Schema**: Normalisasi lebih lanjut pada dimensi
  - **Fact Constellation/Galaxy Schema**: Min. 2 tabel fakta yang berbagi dimensi
- Dokumentasikan alasan pemilihan model dan struktur
- Pastikan diagram mencakup:
  - Semua tabel dengan nama kolom
  - Tipe data setiap kolom
  - Primary keys & Foreign keys
  - Relasi antar tabel

### 1.3 Script DDL untuk DuckDB
- Buat script **SQL Data Definition Language (DDL)** untuk membuat tabel di DuckDB
- Harus mencakup:
  - `CREATE TABLE` untuk semua tabel dimensi dan fakta
  - Definisi **constraints** (Primary Key, Foreign Key, Unique, Not Null)
  - Implementasi **Slowly Changing Dimension (SCD) Type 2**

---

## 📂 Bagian 2: ETL (Extract, Transform, Load) Process

### 2.1 Dataset Sumber
- Identifikasi & dokumentasikan dataset yang digunakan
- Opsi dataset:
  - Dataset publik (Kaggle, data.gov, dll.)
  - Data sintetis yang realistis
  - Kombinasi dari keduanya
- Deskripsi dataset mencakup:
  - Nama & sumber dataset
  - Struktur data (skema, format)
  - Volume data (jumlah record)

### 2.2 Script ETL dengan Python/pandas
- Implementasi proses **ETL lengkap** dengan Python & Pandas
- Script harus mencakup:
  - **Extract**: Mengambil data dari sumber (CSV, API, database)
  - **Transform**:
    - Pembersihan data (handling null, duplikat, inkonsistensi)
    - Transformasi format (konversi tipe data, standarisasi nilai)
    - Pemetaan nilai & penerapan logika bisnis
    - Agregasi & perhitungan tambahan jika diperlukan
  - **Load**: Memuat data ke DuckDB
- Organisasikan kode dengan **fungsi terpisah** untuk setiap tahap
- Implementasikan **logging & error handling**

### 2.3 Implementasi Fitur ETL Lanjutan
- Implementasikan minimal **2 fitur lanjutan** berikut:
  - ETL inkremental (memproses hanya data baru)
  - Implementasi **SCD Type 2** untuk perubahan historis pada dimensi
  - Otomatisasi pipeline dengan **class ETL**

### 2.4 Hasil Akhir di DuckDB
- Demonstrasikan bahwa data berhasil dimuat ke DuckDB
- Buat screenshot atau output yang menunjukkan:
  - **Jumlah record** di setiap tabel
  - **Sampel data** dari setiap tabel

---

## 🎯 Deliverables
1. **Dokumen Kebutuhan Bisnis** (PDF/Word, maks. 3 halaman)
2. **Diagram Skema Data Warehouse** (Image file atau URL)
3. **Script SQL DDL** (`.sql` file)
4. **Deskripsi Dataset** (PDF/Word, maks. 2 halaman)
5. **Script ETL Python** (`.py` atau `.ipynb` file)

---

## 📌 Petunjuk Tambahan
- Gunakan **Git** untuk version control selama pengembangan
- Dokumentasikan semua asumsi yang dibuat
- Fokus pada **integritas & konsistensi data**

---

## 📅 Deadline
- **Waktu Pengumpulan**: 22 Maret 2025
- **Metode**: Kirim tautan GitHub atau penyedia Git lainnya

---

## 🛠 Teknologi yang Digunakan
- **Database**: DuckDB
- **ETL**: Python, Pandas
- **Diagram**: draw.io / dbdiagram.io
- **Version Control**: GitHub
