import duckdb

conn = duckdb.connect(r"D:\Kuliah_Master_UGM\Semester 2\DWIB\DWIB\Airflow\dags\database.duckdb")

# Lihat semua tabel
tables = conn.execute("SHOW TABLES").fetchall()
print("Tabel tersedia:", tables)

# Lihat isi dari satu tabel (misalnya dim_customer)
sample = conn.execute("SELECT * FROM dim_customer LIMIT 5").fetchdf()
print("\nSample data dari fact_transactions:")
print(sample)

# Cek duplikat customer_key
dupes = conn.execute("""
    SELECT customer_key, COUNT(*) AS jumlah
    FROM dim_customer
    GROUP BY customer_key
    HAVING COUNT(*) > 1
""").fetchdf()

# Tampilkan hasil
if not dupes.empty:
    print(f"\n❌ Ditemukan {len(dupes)} customer_key yang duplikat!")
    print(dupes.head())

    # Simpan ke CSV
    dupes.to_csv("duplicate_customer_keys.csv", index=False)
    print("📁 Duplikat disimpan ke: duplicate_customer_keys.csv")
else:
    print("\n✅ Tidak ada customer_key yang duplikat.")

# Tutup koneksi
conn.close()
