import sqlite3

koneksi = sqlite3.connect("database.db")

cursor = koneksi.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS data_siswa (
    no INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    kelas TEXT NOT NULL,
    nilai_tugas INTEGER,
    waktu_pengerjaan TEXT,
    perasaan TEXT
)
""")

koneksi.commit()

koneksi.close()

print("Database berhasil dibuat!")
print("Tabel data_siswa berhasil dibuat!")