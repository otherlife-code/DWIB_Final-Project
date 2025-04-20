import sqlite3

# Path ke database SQLite
db_path = 'data/database_baru.sqlite'  # sesuaikan jika path-nya berbeda

# Koneksi ke database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Ambil semua tabel dan view
cursor.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table', 'view') AND name NOT LIKE 'sqlite_%' ORDER BY type, name;")
objects = cursor.fetchall()

print("📋 Daftar Objek (Tabel & View):")
for name, obj_type in objects:
    print(f"- [{obj_type.upper()}] {name}")

# Tampilkan isi 5 baris pertama dari tiap tabel/view
print("\n📦 Contoh Isi:")
for name, obj_type in objects:
    print(f"\n🔹 {obj_type.capitalize()}: {name}")
    try:
        cursor.execute(f"SELECT * FROM {name} LIMIT 5;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print(f"⚠️ Gagal baca: {e}")

# Tutup koneksi
conn.close()
