import streamlit as st
import sqlite3
def buat_tabel_database():
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

buat_tabel_database()
from datetime import datetime
import pandas as pd


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Belajar Teks Deskripsi",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# DATABASE
# =========================================================

def simpan_data_siswa(nama, kelas, nilai=None, perasaan=None):
    try:
        koneksi = sqlite3.connect("database.db")
        cursor = koneksi.cursor()

        cursor.execute("""
            INSERT INTO data_siswa
            (nama, kelas, nilai_tugas, waktu_pengerjaan, perasaan)
            VALUES (?, ?, ?, ?, ?)
        """, (
            nama,
            kelas,
            nilai,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            perasaan
        ))

        id_siswa = cursor.lastrowid
        koneksi.commit()
        koneksi.close()
        return id_siswa

    except Exception as e:
        st.warning(f"Data belum dapat disimpan ke database: {e}")
        return None


def update_data_siswa(id_siswa, nilai=None, perasaan=None):
    try:
        koneksi = sqlite3.connect("database.db")
        cursor = koneksi.cursor()

        cursor.execute("""
            UPDATE data_siswa
            SET nilai_tugas = ?,
                waktu_pengerjaan = ?,
                perasaan = ?
            WHERE no = ?
        """, (
            nilai,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            perasaan,
            id_siswa
        ))

        koneksi.commit()
        koneksi.close()
        return True

    except Exception as e:
        st.warning(f"Data belum dapat diperbarui: {e}")
        return False


def update_nilai_siswa(id_siswa, nilai):
    try:
        koneksi = sqlite3.connect("database.db")
        cursor = koneksi.cursor()

        cursor.execute("""
            UPDATE data_siswa
            SET nilai_tugas = ?
            WHERE no = ?
        """, (nilai, id_siswa))

        koneksi.commit()
        koneksi.close()
        return True

    except Exception as e:
        st.warning(f"Nilai belum dapat disimpan: {e}")
        return False


def update_refleksi(id_siswa, perasaan):
    try:
        koneksi = sqlite3.connect("database.db")
        cursor = koneksi.cursor()

        cursor.execute("""
            UPDATE data_siswa
            SET perasaan = ?,
                waktu_pengerjaan = ?
            WHERE no = ?
        """, (
            perasaan,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            id_siswa
        ))

        koneksi.commit()
        koneksi.close()
        return True

    except Exception as e:
        st.warning(f"Refleksi belum dapat disimpan: {e}")
        return False


def ambil_semua_data_siswa():
    try:
        koneksi = sqlite3.connect("database.db")
        query = """
            SELECT
                no,
                nama,
                kelas,
                nilai_tugas,
                waktu_pengerjaan,
                perasaan
            FROM data_siswa
            ORDER BY no DESC
        """
        data = pd.read_sql_query(query, koneksi)
        koneksi.close()
        return data

    except Exception as e:
        st.error(f"Data siswa belum dapat dibaca: {e}")
        return pd.DataFrame(
            columns=[
                "no",
                "nama",
                "kelas",
                "nilai_tugas",
                "waktu_pengerjaan",
                "perasaan"
            ]
        )


# =========================================================
# SESSION STATE
# =========================================================

if "login" not in st.session_state:
    st.session_state.login = False

if "login_guru" not in st.session_state:
    st.session_state.login_guru = False

if "jenis_login" not in st.session_state:
    st.session_state.jenis_login = None

if "halaman" not in st.session_state:
    st.session_state.halaman = "login"

if "nama_siswa" not in st.session_state:
    st.session_state.nama_siswa = ""

if "kelas_siswa" not in st.session_state:
    st.session_state.kelas_siswa = ""

if "id_siswa" not in st.session_state:
    st.session_state.id_siswa = None

if "perasaan" not in st.session_state:
    st.session_state.perasaan = ""

if "isi_refleksi" not in st.session_state:
    st.session_state.isi_refleksi = ""

if "hasil_tugas" not in st.session_state:
    st.session_state.hasil_tugas = None


# =========================================================
# DESAIN PASTEL + EFEK 3D
# =========================================================

def desain_halaman(
    warna1="#FAF9F6",
    warna2="#F3F8F3",
    aksen="#7DAF88",
    tombol1="#CFE8D5",
    tombol2="#A9D5B3",
    bayangan="#7FA889"
):
    st.markdown(
        f"""
        <style>
        * {{
            font-family: "Times New Roman", Times, serif !important;
        }}

        html, body {{
            font-family: "Times New Roman", Times, serif !important;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 10% 10%, {warna2} 0%, transparent 30%),
                radial-gradient(circle at 90% 20%, {warna1} 0%, transparent 35%),
                linear-gradient(135deg, {warna1}, #FFFFFF, {warna2});
        }}

        .main .block-container {{
            max-width: 1250px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }}

        [data-testid="stSidebar"] {{
            display: none;
        }}

        h1 {{
            color: #40556A !important;
            font-size: 42px !important;
            font-weight: bold !important;
            text-align: center;
        }}

        h2 {{
            color: #40556A !important;
            font-size: 31px !important;
            font-weight: bold !important;
        }}

        h3 {{
            color: {aksen} !important;
            font-size: 25px !important;
            font-weight: bold !important;
        }}

        p, li, label {{
            color: #344054 !important;
            font-size: 18px !important;
            line-height: 1.75 !important;
        }}

        div.stButton > button {{
            width: 100%;
            min-height: 58px;
            background: linear-gradient(145deg, {tombol1}, {tombol2}) !important;
            color: #344054 !important;
            border: 2px solid rgba(255,255,255,0.95) !important;
            border-radius: 18px !important;
            font-family: "Times New Roman", Times, serif !important;
            font-size: 18px !important;
            font-weight: bold !important;
            box-shadow:
                0 7px 0 {bayangan},
                0 12px 22px rgba(80, 90, 100, 0.16) !important;
            transition: all 0.18s ease-in-out !important;
        }}

        div.stButton > button:hover {{
            transform: translateY(-4px) !important;
            box-shadow:
                0 10px 0 {bayangan},
                0 17px 28px rgba(80, 90, 100, 0.20) !important;
        }}

        div.stButton > button:active {{
            transform: translateY(4px) !important;
            box-shadow:
                0 3px 0 {bayangan},
                0 7px 12px rgba(80, 90, 100, 0.15) !important;
        }}

        div[data-baseweb="input"] > div {{
            border-radius: 14px !important;
            border: 2px solid #D8E1E8 !important;
            background: rgba(255,255,255,0.88) !important;
        }}

        div[data-baseweb="select"] > div {{
            border-radius: 14px !important;
            border: 2px solid #D8E1E8 !important;
            background: rgba(255,255,255,0.88) !important;
        }}

        textarea {{
            border-radius: 15px !important;
        }}

        div[data-testid="stRadio"] label {{
            font-size: 17px !important;
        }}

        div[data-testid="stAlert"] {{
            border-radius: 18px !important;
            font-size: 17px !important;
        }}

        [data-testid="stTable"] {{
            border-radius: 15px !important;
            overflow: hidden !important;
        }}

        a {{
            color: #557A9A !important;
            font-weight: bold !important;
        }}

        [data-testid="stMetric"] {{
            background: rgba(255,255,255,0.78);
            border: 2px solid rgba(255,255,255,0.9);
            border-radius: 18px;
            padding: 15px;
            box-shadow: 0 8px 20px rgba(80,90,100,0.10);
        }}

        [data-testid="stDataFrame"] {{
            border-radius: 18px !important;
            overflow: hidden !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# NAVIGASI
# =========================================================

def kembali_ke_beranda():
    st.session_state.halaman = "home"
    st.rerun()


def keluar():
    st.session_state.login = False
    st.session_state.login_guru = False
    st.session_state.jenis_login = None
    st.session_state.halaman = "login"

    st.session_state.nama_siswa = ""
    st.session_state.kelas_siswa = ""
    st.session_state.id_siswa = None
    st.session_state.perasaan = ""
    st.session_state.isi_refleksi = ""
    st.session_state.hasil_tugas = None

    st.rerun()


def keluar_guru():
    st.session_state.login_guru = False
    st.session_state.login = False
    st.session_state.jenis_login = None
    st.session_state.halaman = "login"
    st.rerun()


# =========================================================
# HALAMAN PILIH AKSES
# =========================================================

def halaman_login():

    desain_halaman(
        warna1="#FFF4F7",
        warna2="#F3EAF5",
        aksen="#B86F85",
        tombol1="#F2D2DC",
        tombol2="#E7B8C8",
        bayangan="#B86F85"
    )

    st.write("🌸 🌷 🌼 ✿ 🌷 🌸")

    st.title("🌸 Belajar Teks Deskripsi 🌸")

    st.subheader(
        "✨ Media Pembelajaran Bahasa Indonesia Kelas IX SMP ✨"
    )

    st.info(
        "Selamat datang di media pembelajaran digital Teks Deskripsi. "
        "Silakan pilih akses sesuai peranmu."
    )

    st.write("")
    st.subheader("🌷 Pilih Akses")

    kolom1, kolom2 = st.columns(2)

    with kolom1:
        st.subheader("👩‍🎓 Siswa")
        st.write(
            "Masuk untuk mengikuti pembelajaran, membaca materi, "
            "mengerjakan tugas, dan mengisi refleksi."
        )

        if st.button("👩‍🎓 Masuk sebagai Siswa", key="akses_siswa"):
            st.session_state.jenis_login = "siswa"
            st.session_state.halaman = "login_siswa"
            st.rerun()

    with kolom2:
        st.subheader("👩‍🏫 Guru")
        st.write(
            "Masuk untuk melihat data siswa, nilai tugas, "
            "refleksi, dan waktu pengerjaan."
        )

        if st.button("👩‍🏫 Masuk sebagai Guru", key="akses_guru"):
            st.session_state.jenis_login = "guru"
            st.session_state.halaman = "login_guru"
            st.rerun()

    st.write("")
    st.write("🌼 Belajar dengan membaca, mengamati, mencoba, dan berefleksi. 🌼")


# =========================================================
# LOGIN SISWA
# =========================================================

def halaman_login_siswa():

    desain_halaman(
        warna1="#FFF4F7",
        warna2="#F3EAF5",
        aksen="#B86F85",
        tombol1="#F2D2DC",
        tombol2="#E7B8C8",
        bayangan="#B86F85"
    )

    st.write("🌸 🌷 🌼 ✿ 🌷 🌸")
    st.title("👩‍🎓 Login Siswa")

    st.info(
        "Silakan masukkan username dan password untuk "
        "masuk ke pembelajaran."
    )

    kolom1, kolom2, kolom3 = st.columns([1, 2, 1])

    with kolom2:

        username = st.text_input(
            "👤 Username",
            placeholder="Masukkan username",
            key="login_siswa_username"
        )

        password = st.text_input(
            "🔐 Password",
            type="password",
            placeholder="Masukkan password",
            key="login_siswa_password"
        )

        if st.button("🌷 Masuk ke Pembelajaran", key="tombol_login_siswa"):

            if username.strip() == st.secrets["USERNAME"].strip() and password.strip() == st.secrets["PASSWORD"].strip():

                st.session_state.login = True
                st.session_state.login_guru = False
                st.session_state.jenis_login = "siswa"
                st.session_state.halaman = "identitas"
                st.rerun()

            else:
                st.error("Username atau password belum sesuai.")

        if st.button("🏠 Kembali Pilih Akses", key="kembali_pilih_akses_siswa"):
            st.session_state.halaman = "login"
            st.session_state.jenis_login = None
            st.rerun()


# =========================================================
# LOGIN GURU
# =========================================================

def halaman_login_guru():

    desain_halaman(
        warna1="#F4F0FA",
        warna2="#E9E0F5",
        aksen="#8068A8",
        tombol1="#DDD3F2",
        tombol2="#C9BAE5",
        bayangan="#8068A8"
    )

    st.write("🌸 💜 🌷 ✿ 🌼 💜 🌸")
    st.title("👩‍🏫 Login Guru")

    st.info(
        "Selamat datang di halaman guru. Silakan masuk untuk "
        "melihat data pembelajaran siswa."
    )

    kolom1, kolom2, kolom3 = st.columns([1, 2, 1])

    with kolom2:

        username = st.text_input(
            "👤 Username Guru",
            placeholder="Masukkan username guru",
            key="login_guru_username"
        )

        password = st.text_input(
            "🔐 Password Guru",
            type="password",
            placeholder="Masukkan password guru",
            key="login_guru_password"
        )

        if st.button("🌷 Masuk ke Dashboard Guru", key="tombol_login_guru"):

            if username == "Kelompok C" and password == "Guru Cantik":

                st.session_state.login_guru = True
                st.session_state.login = False
                st.session_state.jenis_login = "guru"
                st.session_state.halaman = "dashboard_guru"
                st.rerun()

            else:
                st.error("Username atau password guru belum sesuai.")

        if st.button("🏠 Kembali Pilih Akses", key="kembali_pilih_akses_guru"):
            st.session_state.halaman = "login"
            st.session_state.jenis_login = None
            st.rerun()


# =========================================================
# IDENTITAS
# =========================================================

def halaman_identitas():

    desain_halaman(
        warna1="#EFF8FC",
        warna2="#E8F4F8",
        aksen="#6498B5",
        tombol1="#D3EAF5",
        tombol2="#B9DCEC",
        bayangan="#6498B5"
    )

    st.write("🌸 🌿 🌼 🌷 🌿 🌸")
    st.title("👤 Identitas Siswa")

    st.info(
        "Sebelum memulai pembelajaran, silakan isi identitas kamu "
        "dengan benar."
    )

    nama = st.text_input(
        "🌷 Nama Lengkap",
        value=st.session_state.nama_siswa,
        placeholder="Tuliskan nama lengkap"
    )

    kelas = st.selectbox(
        "🏫 Kelas",
        ["IX A", "IX B", "IX C", "IX D", "IX E", "IX F"]
    )

    if st.button("✨ Simpan & Mulai Belajar"):

        if nama.strip() == "":
            st.warning("Nama lengkap harus diisi terlebih dahulu.")

        else:
            st.session_state.nama_siswa = nama.strip()
            st.session_state.kelas_siswa = kelas

            id_baru = simpan_data_siswa(
                nama.strip(),
                kelas
            )

            if id_baru is not None:
                st.session_state.id_siswa = id_baru
                st.session_state.halaman = "home"

                st.success("🌸 Identitas berhasil disimpan.")
                st.rerun()


# =========================================================
# BERANDA
# =========================================================

def halaman_home():

    desain_halaman(
        warna1="#FAF9F6",
        warna2="#F2F8F4",
        aksen="#6B9B78",
        tombol1="#CFE8D5",
        tombol2="#B7DEC0",
        bayangan="#7FA889"
    )

    st.write("🌸 🌷 🌼 🌿 ✿ 🌸 🌷 🌼 🌿 ✿")
    st.title("🌸 Beranda Pembelajaran 🌸")

    st.subheader(
        f"Selamat datang, {st.session_state.nama_siswa}! 👋"
    )

    st.write(f"Kelas: {st.session_state.kelas_siswa}")

    st.info(
        "Yuk belajar Teks Deskripsi dengan membaca materi, "
        "melihat contoh, mengerjakan tugas, memahami rubrik penilaian, "
        "dan melakukan refleksi pembelajaran. 🌷"
    )

    kolom1, kolom2, kolom3 = st.columns(3)

    with kolom1:
        st.subheader("📖 Materi")
        st.write(
            "Pelajari pengertian, tujuan, ciri, struktur, "
            "unsur kebahasaan, hingga langkah menulis teks deskripsi."
        )

        if st.button("📖 Buka Materi", key="home_materi"):
            st.session_state.halaman = "materi"
            st.rerun()

    with kolom2:
        st.subheader("🎬 Contoh")
        st.write(
            "Amati contoh pembelajaran melalui video YouTube "
            "untuk membantu memahami Teks Deskripsi."
        )

        if st.button("🎬 Lihat Contoh", key="home_contoh"):
            st.session_state.halaman = "contoh"
            st.rerun()

    with kolom3:
        st.subheader("📝 Tugas")
        st.write("Kerjakan 20 soal pilihan ganda melalui Wayground.")

        if st.button("📝 Kerjakan Tugas", key="home_tugas"):
            st.session_state.halaman = "tugas"
            st.rerun()

    st.write("")

    kolom4, kolom5, kolom6 = st.columns(3)

    with kolom4:
        st.subheader("📊 Rubrik")
        st.write(
            "Lihat pedoman penilaian tugas pilihan ganda "
            "yang terdiri dari 20 soal."
        )

        if st.button("📊 Lihat Rubrik", key="home_rubrik"):
            st.session_state.halaman = "rubrik"
            st.rerun()

    with kolom5:
        st.subheader("😊 Refleksi")
        st.write(
            "Pilih stiker perasaanmu hari ini dan tuliskan "
            "pengalamanmu setelah belajar."
        )

        if st.button("😊 Refleksi", key="home_refleksi"):
            st.session_state.halaman = "refleksi"
            st.rerun()

    with kolom6:
        st.subheader("👤 Identitas")
        st.write(f"Nama: {st.session_state.nama_siswa}")
        st.write(f"Kelas: {st.session_state.kelas_siswa}")

    st.write("")

    st.write(
        "🌷 Pilih menu di atas untuk mulai belajar. "
        "Jangan lupa membaca materi sebelum mengerjakan tugas. 🌷"
    )

    if st.button("🚪 Keluar"):
        keluar()


# =========================================================
# DASHBOARD GURU
# =========================================================

def halaman_dashboard_guru():

    desain_halaman(
        warna1="#F8F5FD",
        warna2="#EEE8F8",
        aksen="#8068A8",
        tombol1="#DDD3F2",
        tombol2="#C9BAE5",
        bayangan="#8068A8"
    )

    st.write("🌸 💜 🌷 ✿ 🌼 💜 🌸")
    st.title("👩‍🏫 Dashboard Guru")
    st.subheader("📊 Data Pembelajaran Siswa")

    st.info(
        "Halaman ini menampilkan data siswa yang tersimpan "
        "di database pembelajaran."
    )

    data = ambil_semua_data_siswa()

    jumlah_siswa = len(data)

    if not data.empty and data["nilai_tugas"].notna().any():
        rata_rata = data["nilai_tugas"].dropna().mean()
        rata_rata_tampil = f"{rata_rata:.1f}"
    else:
        rata_rata_tampil = "—"

    if not data.empty:
        jumlah_nilai = int(data["nilai_tugas"].notna().sum())
    else:
        jumlah_nilai = 0

    kolom1, kolom2, kolom3 = st.columns(3)

    with kolom1:
        st.metric("👥 Jumlah Data Siswa", jumlah_siswa)

    with kolom2:
        st.metric("📊 Siswa Sudah Dinilai", jumlah_nilai)

    with kolom3:
        st.metric("📈 Rata-Rata Nilai", rata_rata_tampil)

    st.write("")
    st.subheader("🌷 Daftar Data Siswa")

    if data.empty:
        st.warning(
            "Belum ada data siswa yang tersimpan di database."
        )

    else:
        data_tampil = data.rename(
            columns={
                "no": "🔢 ID Data Siswa",
                "nama": "👤 Nama Siswa",
                "kelas": "🏫 Kelas",
                "nilai_tugas": "📊 Nilai Tugas",
                "waktu_pengerjaan": "🕐 Waktu Pengerjaan",
                "perasaan": "😊 Perasaan / Refleksi"
            }
        )

        st.dataframe(
            data_tampil,
            use_container_width=True,
            hide_index=True
        )

        st.write("")
        st.subheader("🌼 Ringkasan Nilai")

        nilai_data = data[data["nilai_tugas"].notna()].copy()

        if nilai_data.empty:
            st.info(
                "Belum ada nilai tugas yang tersimpan."
            )
        else:
            st.bar_chart(
                nilai_data.set_index("nama")["nilai_tugas"]
            )

        st.write("")
        st.subheader("🌸 Keterangan")

        st.write(
            "• 👤 Nama siswa: nama lengkap yang diisi siswa."
        )
        st.write(
            "• 🏫 Kelas: kelas siswa."
        )
        st.write(
            "• 📊 Nilai tugas: nilai yang dimasukkan siswa setelah "
            "mengerjakan Wayground."
        )
        st.write(
            "• 😊 Perasaan/refleksi: stiker perasaan dan tulisan "
            "refleksi siswa."
        )
        st.write(
            "• 🕐 Waktu pengerjaan: waktu terakhir data siswa "
            "atau refleksi diperbarui."
        )
        st.write(
            "• 🔢 ID data siswa: nomor unik setiap data siswa."
        )

        st.write("")
        st.subheader("💾 Unduh Data")

        csv_data = data.to_csv(index=False).encode("utf-8-sig")

        st.download_button(
            "📥 Download Data Siswa (CSV)",
            data=csv_data,
            file_name="data_siswa_teks_deskripsi.csv",
            mime="text/csv",
            key="download_csv"
        )

    st.write("")
    st.write("🌷 Data diambil langsung dari database pembelajaran. 🌷")

    kolom_bawah1, kolom_bawah2 = st.columns(2)

    with kolom_bawah1:
        if st.button("🔄 Refresh Data", key="refresh_data_guru"):
            st.rerun()

    with kolom_bawah2:
        if st.button("🚪 Keluar dari Dashboard Guru", key="keluar_guru"):
            keluar_guru()


# =========================================================
# MATERI
# =========================================================

def halaman_materi():

    desain_halaman(
        warna1="#F2FAF3",
        warna2="#E8F5EB",
        aksen="#6B9B78",
        tombol1="#CFE8D5",
        tombol2="#B7DEC0",
        bayangan="#7FA889"
    )

    st.write("🌿 🌸 🌼 🌷 🌿 🌸")
    st.title("📖 Materi Teks Deskripsi")

    st.info(
        "Bacalah materi secara berurutan. Materi ini membahas "
        "Teks Deskripsi mulai dari pengertian sampai langkah "
        "menulisnya."
    )

    st.header("1. Pengertian Teks Deskripsi")
    st.write(
        "Teks deskripsi adalah teks yang menggambarkan suatu objek "
        "secara jelas dan terperinci sehingga pembaca seolah-olah "
        "dapat melihat, mendengar, merasakan, atau mengalami sendiri "
        "objek yang sedang dijelaskan."
    )
    st.write(
        "Objek yang dideskripsikan dapat berupa tempat, benda, "
        "hewan, tumbuhan, seseorang, suasana, maupun objek lain "
        "yang dapat diamati."
    )
    st.write(
        "Penulis menggunakan kata-kata yang spesifik agar pembaca "
        "memperoleh gambaran yang jelas mengenai objek tersebut."
    )
    st.write(
        "Teks deskripsi tidak hanya menyebutkan nama objek. "
        "Penulis juga menjelaskan bentuk, warna, ukuran, keadaan, "
        "suasana, sifat, serta ciri khas objek."
    )

    st.header("2. Tujuan Teks Deskripsi")
    st.write(
        "Tujuan utama teks deskripsi adalah memberikan gambaran "
        "yang jelas dan terperinci mengenai suatu objek kepada "
        "pembaca."
    )
    st.subheader("🌷 Beberapa tujuan teks deskripsi")
    st.write("• Menggambarkan objek secara jelas.")
    st.write("• Membantu pembaca mengenali ciri-ciri suatu objek.")
    st.write("• Membuat pembaca seolah-olah dapat melihat objek.")
    st.write("• Menjelaskan keadaan atau suasana suatu tempat.")
    st.write("• Memberikan kesan tertentu kepada pembaca.")
    st.write("• Membantu pembaca membayangkan objek.")

    st.header("3. Ciri-Ciri Teks Deskripsi")
    st.write(
        "Teks deskripsi memiliki beberapa ciri yang membedakannya "
        "dari jenis teks lainnya. Ciri-ciri tersebut berkaitan "
        "dengan objek yang dijelaskan, cara penyampaian, dan "
        "penggunaan bahasa."
    )
    st.subheader("🌼 Ciri-ciri utama")
    st.write("1. Menggambarkan suatu objek secara khusus.")
    st.write("2. Menyajikan informasi secara rinci.")
    st.write("3. Menggunakan kata-kata yang menggambarkan keadaan objek.")
    st.write("4. Banyak menggunakan kata sifat atau adjektiva.")
    st.write("5. Menggunakan kata yang berkaitan dengan pancaindra.")
    st.write("6. Menggunakan kalimat konkret.")
    st.write("7. Membantu pembaca membayangkan objek.")
    st.write("8. Dapat menampilkan kesan atau perasaan penulis.")
    st.success(
        "💡 Intinya, teks deskripsi membuat pembaca mendapatkan "
        "gambaran yang lebih jelas mengenai suatu objek."
    )

    st.header("4. Struktur Teks Deskripsi")
    st.write(
        "Struktur teks adalah susunan bagian-bagian yang membentuk "
        "teks secara utuh. Teks deskripsi umumnya terdiri atas "
        "identifikasi, deskripsi bagian, dan simpulan atau kesan."
    )
    st.subheader("🌷 A. Identifikasi")
    st.write(
        "Identifikasi merupakan bagian awal teks deskripsi. "
        "Pada bagian ini penulis memperkenalkan objek yang "
        "akan dideskripsikan."
    )
    st.write(
        "Informasi dapat berupa nama objek, lokasi objek, jenis "
        "objek, atau gambaran umum mengenai objek."
    )
    st.subheader("🌼 B. Deskripsi Bagian")
    st.write(
        "Deskripsi bagian merupakan bagian yang menjelaskan objek "
        "secara lebih rinci."
    )
    st.write(
        "Penulis dapat menjelaskan bentuk, warna, ukuran, kondisi, "
        "bagian-bagian objek, suasana, maupun karakteristik khusus."
    )
    st.write(
        "Bagian ini biasanya menjadi bagian yang paling banyak "
        "karena penulis perlu memberikan informasi yang cukup "
        "agar pembaca dapat membayangkan objek."
    )
    st.subheader("🌸 C. Simpulan atau Kesan")
    st.write(
        "Simpulan atau kesan merupakan bagian penutup yang berisi "
        "kesan penulis terhadap objek yang telah dideskripsikan."
    )
    st.write(
        "Kesan dapat berupa perasaan, pendapat, atau tanggapan "
        "penulis terhadap objek."
    )

    st.header("5. Unsur Kebahasaan Teks Deskripsi")
    st.write(
        "Bahasa dalam teks deskripsi harus mampu membantu pembaca "
        "membayangkan objek. Oleh karena itu, pemilihan kata "
        "menjadi sangat penting."
    )
    st.subheader("🌿 A. Kata Sifat")
    st.write(
        "Kata sifat digunakan untuk menjelaskan keadaan atau "
        "karakteristik objek."
    )
    st.write(
        "Contoh: indah, luas, bersih, sejuk, tinggi, besar, "
        "tenang, ramai, lembut, cerah, dan nyaman."
    )
    st.subheader("🌿 B. Kata Khusus")
    st.write(
        "Kata khusus memberikan informasi yang lebih spesifik "
        "daripada kata umum."
    )
    st.write(
        "Contohnya, daripada hanya menggunakan kata 'bunga', "
        "penulis dapat menggunakan 'mawar merah', 'melati putih', "
        "atau 'anggrek ungu'."
    )
    st.subheader("🌿 C. Kata yang Berkaitan dengan Pancaindra")
    st.write(
        "Penggunaan pancaindra membantu pembaca membayangkan "
        "objek dengan lebih jelas."
    )
    st.write("👁 Penglihatan: cerah, hijau, berkilauan.")
    st.write("👂 Pendengaran: gemericik, riuh, merdu.")
    st.write("👃 Penciuman: harum, wangi, menyengat.")
    st.write("🖐 Perabaan: lembut, kasar, dingin, hangat.")
    st.write("👅 Pengecapan: manis, asin, asam, pahit.")

    st.header("6. Kalimat Konkret")
    st.write(
        "Kalimat konkret adalah kalimat yang menggambarkan objek "
        "dengan informasi yang dapat diamati atau dibayangkan "
        "secara jelas."
    )
    st.write(
        "Kalimat konkret membuat informasi menjadi lebih spesifik "
        "sehingga pembaca tidak memperoleh gambaran yang terlalu "
        "umum."
    )
    st.success(
        "Contoh: Air Danau Toba tampak biru dan tenang di bawah "
        "cahaya matahari pagi."
    )

    st.header("7. Kalimat Perincian")
    st.write(
        "Kalimat perincian digunakan untuk menjelaskan suatu "
        "objek secara lebih detail."
    )
    st.write(
        "Misalnya, jika penulis mengatakan bahwa sebuah taman "
        "sangat indah, pernyataan tersebut dapat diperinci "
        "dengan menjelaskan warna bunga, kondisi rumput, "
        "suara burung, aroma tanaman, dan keadaan lingkungan."
    )
    st.success(
        "Contoh: Bunga-bunga merah, kuning, dan putih tumbuh "
        "di sepanjang sisi taman. Rumputnya hijau dan terawat."
    )

    st.header("8. Majas Personifikasi")
    st.write(
        "Majas personifikasi adalah gaya bahasa yang memberikan "
        "sifat atau perilaku manusia kepada benda mati atau "
        "fenomena alam."
    )
    st.write(
        "Penggunaan personifikasi dapat membuat teks deskripsi "
        "menjadi lebih hidup dan menarik."
    )
    st.success(
        "Contoh: Angin pagi menyapa wajahku dengan lembut."
    )
    st.write(
        "Angin sebenarnya tidak dapat menyapa seperti manusia. "
        "Kata 'menyapa' digunakan untuk memberikan kesan "
        "yang lebih hidup."
    )

    st.header("9. Penggunaan Pancaindra")
    st.write(
        "Salah satu hal penting dalam menulis teks deskripsi "
        "adalah memanfaatkan pengalaman pancaindra."
    )
    st.subheader("👁 Penglihatan")
    st.write(
        "Digunakan untuk menggambarkan warna, bentuk, ukuran, "
        "jarak, cahaya, dan keadaan."
    )
    st.subheader("👂 Pendengaran")
    st.write(
        "Digunakan untuk menggambarkan suara, bunyi, musik, "
        "kicauan, gemericik, dan keramaian."
    )
    st.subheader("👃 Penciuman")
    st.write(
        "Digunakan untuk menggambarkan aroma, bau, wangi, "
        "harum, dan sebagainya."
    )
    st.subheader("🖐 Perabaan")
    st.write(
        "Digunakan untuk menggambarkan tekstur, suhu, "
        "kelembutan, dan kekasaran."
    )
    st.subheader("👅 Pengecapan")
    st.write(
        "Digunakan untuk menggambarkan rasa seperti manis, "
        "asin, pahit, asam, dan gurih."
    )

    st.header("10. Contoh Teks Deskripsi")
    st.subheader("🌊 Danau Toba")
    st.write(
        "Danau Toba merupakan salah satu danau yang terkenal "
        "di Indonesia. Danau ini memiliki pemandangan alam "
        "yang luas dan menarik karena perpaduan antara air "
        "danau, pegunungan, serta langit yang membentang "
        "di sekitarnya."
    )
    st.write(
        "Pada pagi hari, permukaan air Danau Toba tampak "
        "tenang. Warna airnya terlihat biru dengan pantulan "
        "cahaya matahari yang membuat permukaannya tampak "
        "berkilauan."
    )
    st.write(
        "Udara di sekitar danau terasa sejuk, terutama ketika "
        "angin bertiup perlahan."
    )
    st.write(
        "Di kejauhan terlihat perbukitan yang menghijau. "
        "Pepohonan tumbuh di beberapa bagian wilayah sekitar "
        "danau sehingga pemandangan terlihat lebih alami."
    )
    st.write(
        "Suasana yang tenang membuat kawasan tersebut terasa "
        "nyaman untuk menikmati keindahan alam."
    )
    st.write(
        "Keindahan Danau Toba membuat tempat ini menjadi salah "
        "satu pemandangan alam yang menarik untuk diamati."
    )

    st.header("11. Analisis Contoh Teks")
    st.subheader("🌷 Identifikasi")
    st.write(
        "Bagian awal memperkenalkan Danau Toba sebagai objek "
        "yang akan dideskripsikan."
    )
    st.subheader("🌼 Deskripsi Bagian")
    st.write(
        "Bagian berikutnya menjelaskan warna air, keadaan "
        "permukaan danau, udara, perbukitan, pepohonan, "
        "dan suasana."
    )
    st.subheader("🌸 Simpulan atau Kesan")
    st.write(
        "Bagian akhir menunjukkan kesan mengenai keindahan "
        "dan kenyamanan pemandangan Danau Toba."
    )
    st.subheader("🌿 Unsur Pancaindra")
    st.write("Penglihatan: biru, hijau, dan berkilauan.")
    st.write("Perabaan: sejuk.")
    st.write("Suasana: tenang dan nyaman.")

    st.header("12. Langkah-Langkah Menulis Teks Deskripsi")
    st.subheader("🌷 Langkah 1 — Menentukan objek")
    st.write(
        "Pilih objek yang akan dideskripsikan, misalnya sekolah, "
        "rumah, taman, tempat wisata, hewan, tumbuhan, atau benda."
    )
    st.subheader("🌷 Langkah 2 — Melakukan pengamatan")
    st.write(
        "Amati objek dengan teliti. Perhatikan bentuk, warna, "
        "ukuran, kondisi, suasana, suara, aroma, tekstur, "
        "dan karakteristik lainnya."
    )
    st.subheader("🌷 Langkah 3 — Mencatat informasi")
    st.write(
        "Tuliskan informasi penting yang ditemukan selama "
        "pengamatan."
    )
    st.subheader("🌷 Langkah 4 — Menentukan struktur")
    st.write(
        "Susun informasi menjadi bagian identifikasi, "
        "deskripsi bagian, dan simpulan atau kesan."
    )
    st.subheader("🌷 Langkah 5 — Memilih kata yang tepat")
    st.write(
        "Gunakan kata sifat, kata khusus, kalimat konkret, "
        "kalimat perincian, serta kata yang berkaitan "
        "dengan pancaindra."
    )
    st.subheader("🌷 Langkah 6 — Menyusun paragraf")
    st.write(
        "Gabungkan informasi menjadi paragraf yang runtut "
        "dan mudah dipahami."
    )
    st.subheader("🌷 Langkah 7 — Memeriksa kembali")
    st.write(
        "Periksa ejaan, tanda baca, pilihan kata, struktur, "
        "dan kelengkapan informasi."
    )

    st.header("13. Tips Menulis Teks Deskripsi")
    st.write("🌷 Amati objek dengan teliti.")
    st.write("🌷 Gunakan kata-kata yang spesifik.")
    st.write("🌷 Hindari penjelasan yang terlalu umum.")
    st.write("🌷 Gunakan pancaindra untuk memperkaya deskripsi.")
    st.write("🌷 Gunakan kalimat perincian.")
    st.write("🌷 Pilih kata sifat yang sesuai.")
    st.write("🌷 Susun informasi secara runtut.")
    st.write(
        "🌷 Buat pembaca seolah-olah berada di tempat atau "
        "melihat objek yang kamu deskripsikan."
    )
    st.write("🌷 Periksa kembali tulisan sebelum dikumpulkan.")

    st.header("14. Ringkasan Materi")
    st.success(
        "Teks deskripsi adalah teks yang menggambarkan suatu "
        "objek secara jelas dan terperinci. Tujuannya agar "
        "pembaca dapat membayangkan objek tersebut."
    )
    st.success(
        "Struktur teks deskripsi meliputi identifikasi, "
        "deskripsi bagian, dan simpulan atau kesan."
    )
    st.success(
        "Dalam menulis teks deskripsi, gunakan kata sifat, "
        "kata khusus, kalimat konkret, kalimat perincian, "
        "majas yang sesuai, serta pengalaman pancaindra."
    )
    st.info(
        "🌸 Setelah memahami materi, lanjutkan ke menu "
        "Contoh untuk melihat video pembelajaran. "
        "Setelah itu kamu dapat mengerjakan Tugas. 🌸"
    )

    if st.button("🏠 Kembali ke Beranda", key="back_materi"):
        kembali_ke_beranda()


# =========================================================
# CONTOH VIDEO YOUTUBE
# =========================================================

def halaman_contoh():

    desain_halaman(
        warna1="#F0FAF9",
        warna2="#E3F3F1",
        aksen="#4E8F8A",
        tombol1="#C7E8E5",
        tombol2="#A9D7D3",
        bayangan="#4E8F8A"
    )

    st.write("🌸 🌿 🌼 🌷 🌿 🌸")
    st.title("🎬 Contoh Teks Deskripsi")

    st.info(
        "Silakan tonton video pembelajaran berikut untuk "
        "melihat contoh Teks Deskripsi."
    )

    st.subheader("🎥 Video Pembelajaran")

    st.video(
        "https://youtu.be/FwghnQCNiAc?si=5EgOMNUTK1fqgw2b"
    )

    st.success(
        "💡 Saat menonton video, perhatikan cara menjelaskan "
        "objek, penggunaan kata sifat, struktur teks, "
        "dan penggunaan pancaindra."
    )

    if st.button("🏠 Kembali ke Beranda", key="back_contoh"):
        kembali_ke_beranda()


# =========================================================
# TUGAS WAYGROUND + INPUT NILAI
# =========================================================

def halaman_tugas():

    desain_halaman(
        warna1="#FFF7F1",
        warna2="#FBEDE4",
        aksen="#C9825F",
        tombol1="#F8D8C4",
        tombol2="#F1BFA4",
        bayangan="#C9825F"
    )

    st.write("🌷 🌸 🌼 📝 🌼 🌸 🌷")
    st.title("📝 Tugas Pilihan Ganda")

    st.info(
        "Tugas terdiri atas 20 soal pilihan ganda yang "
        "dikerjakan melalui Wayground."
    )

    st.subheader("🎯 Petunjuk Pengerjaan")
    st.write("1. Klik tombol untuk membuka tugas.")
    st.write("2. Masukkan kode permainan jika diminta.")
    st.write("3. Bacalah setiap soal dengan teliti.")
    st.write("4. Pilih satu jawaban yang paling sesuai.")
    st.write("5. Kerjakan seluruh 20 soal.")
    st.write("6. Periksa kembali jawaban sebelum mengirimkan.")

    st.subheader("🔑 Kode Tugas")
    st.success("52374125")

    st.subheader("🌐 Buka Tugas di Wayground")

    st.link_button(
        "📝 Buka Tugas Wayground",
        "https://wayground.com/join?gc=52374125&source=liveDashboard"
    )

    st.warning(
        "📌 Tugas terdiri dari 20 soal pilihan ganda. "
        "Setiap soal bernilai 5 poin, sehingga nilai maksimal "
        "adalah 100."
    )

    st.subheader("📊 Perhitungan Nilai")
    st.write("Rumus nilai: Jumlah Jawaban Benar × 5")
    st.write("Contoh: jika benar 16 soal, maka nilai = 16 × 5 = 80.")

    st.subheader("📝 Masukkan Nilai Tugas")
    st.write(
        "Setelah selesai mengerjakan Wayground, masukkan nilai "
        "yang kamu peroleh di sini."
    )

    nilai_masuk = st.number_input(
        "🎯 Nilai yang diperoleh",
        min_value=0,
        max_value=100,
        value=0,
        step=5
    )

    if st.button("💾 Simpan Nilai Tugas", key="simpan_nilai_tugas"):

        if st.session_state.id_siswa is None:
            st.warning(
                "ID siswa tidak ditemukan. Silakan isi identitas "
                "terlebih dahulu."
            )

        else:
            nilai_masuk = int(nilai_masuk)

            berhasil = update_nilai_siswa(
                st.session_state.id_siswa,
                nilai_masuk
            )

            if berhasil:
                st.session_state.hasil_tugas = nilai_masuk

                st.success(
                    f"🌸 Nilai tugas berhasil disimpan: "
                    f"{nilai_masuk}/100"
                )

                st.balloons()

    if st.session_state.hasil_tugas is not None:
        st.info(
            f"📊 Nilai tugas kamu saat ini: "
            f"{st.session_state.hasil_tugas}/100"
        )

    st.success(
        "✨ Setelah menyelesaikan tugas, buka menu Rubrik "
        "untuk melihat kategori nilai."
    )

    if st.button("🏠 Kembali ke Beranda", key="back_tugas"):
        kembali_ke_beranda()


# =========================================================
# RUBRIK
# =========================================================

def halaman_rubrik():

    desain_halaman(
        warna1="#F8F5FD",
        warna2="#EEE8F8",
        aksen="#8068A8",
        tombol1="#DDD3F2",
        tombol2="#C9BAE5",
        bayangan="#8068A8"
    )

    st.write("🌸 💜 🌷 ✿ 🌼 💜 🌸")
    st.title("📊 Rubrik Penilaian Tugas")

    st.info(
        "Rubrik berikut disesuaikan dengan tugas pilihan ganda "
        "yang terdiri dari 20 soal."
    )

    st.subheader("📝 Ketentuan Penilaian")
    st.write("• Jumlah soal: 20 soal")
    st.write("• Bentuk soal: Pilihan Ganda")
    st.write("• Nilai setiap soal: 5 poin")
    st.write("• Nilai maksimal: 100")
    st.write("• Rumus: Jumlah Benar × 5")

    st.subheader("🌷 Kriteria Nilai")

    data_rubrik = {
        "Jumlah Benar": [
            "18–20 soal",
            "15–17 soal",
            "12–14 soal",
            "0–11 soal"
        ],
        "Rentang Nilai": [
            "90–100",
            "75–85",
            "60–70",
            "0–55"
        ],
        "Kategori": [
            "Sangat Baik",
            "Baik",
            "Cukup",
            "Perlu Bimbingan"
        ],
        "Keterangan": [
            "Pemahaman materi sangat baik.",
            "Pemahaman materi sudah baik.",
            "Pemahaman materi cukup dan masih dapat ditingkatkan.",
            "Memerlukan pembelajaran dan pendampingan lebih lanjut."
        ]
    }

    st.table(data_rubrik)

    st.subheader("🌼 Contoh Perhitungan")
    st.write("20 benar → 20 × 5 = 100")
    st.write("18 benar → 18 × 5 = 90")
    st.write("16 benar → 16 × 5 = 80")
    st.write("14 benar → 14 × 5 = 70")
    st.write("10 benar → 10 × 5 = 50")

    st.success(
        "💡 Rubrik ini membantu siswa memahami hubungan antara "
        "jumlah jawaban benar dengan nilai tugas."
    )

    if st.button("🏠 Kembali ke Beranda", key="back_rubrik"):
        kembali_ke_beranda()


# =========================================================
# REFLEKSI
# =========================================================

def halaman_refleksi():

    desain_halaman(
        warna1="#FFF5F8",
        warna2="#F7EAF0",
        aksen="#B86F85",
        tombol1="#F2D2DC",
        tombol2="#E6B8C8",
        bayangan="#B86F85"
    )

    st.write("🌸 🌷 💕 🌼 🌸 🌷 💕 🌼")
    st.title("😊 Refleksi Perasaan Hari Ini")

    st.info(
        "Setelah belajar Teks Deskripsi, pilih stiker yang paling "
        "menggambarkan perasaanmu hari ini. Setelah itu, tuliskan "
        "cerita atau perasaanmu."
    )

    st.subheader("💗 Bagaimana perasaanmu hari ini?")

    pilihan_perasaan = {
        "😄": "Sangat senang",
        "😊": "Senang",
        "🥰": "Semangat",
        "😌": "Tenang",
        "🤔": "Masih berpikir",
        "😐": "Biasa saja",
        "😕": "Sedikit bingung",
        "😴": "Mengantuk",
        "😥": "Sedikit kesulitan"
    }

    stiker = st.selectbox(
        "Pilih satu stiker perasaan:",
        list(pilihan_perasaan.keys())
    )

    st.write(
        f"Perasaanmu: {stiker} {pilihan_perasaan[stiker]}"
    )

    st.subheader("💌 Ceritakan Perasaanmu")

    isi_refleksi = st.text_area(
        "Tuliskan refleksimu di sini:",
        value=st.session_state.isi_refleksi,
        placeholder=(
            "Contoh: Hari ini saya merasa senang karena "
            "sudah memahami struktur teks deskripsi. "
            "Saya masih ingin belajar tentang penggunaan majas."
        ),
        height=180
    )

    st.write(
        "🌷 Kamu boleh menuliskan apa saja yang kamu rasakan "
        "selama mengikuti pembelajaran. 🌷"
    )

    if st.button("💌 Kirim Refleksi"):

        if isi_refleksi.strip() == "":
            st.warning(
                "Silakan tuliskan isi refleksimu terlebih dahulu."
            )

        else:
            st.session_state.perasaan = (
                f"{stiker} {pilihan_perasaan[stiker]}"
            )

            st.session_state.isi_refleksi = isi_refleksi

            data_refleksi = (
                f"{stiker} {pilihan_perasaan[stiker]} - "
                f"{isi_refleksi}"
            )

            if st.session_state.id_siswa is not None:

                berhasil = update_refleksi(
                    st.session_state.id_siswa,
                    data_refleksi
                )

                if berhasil:
                    st.success(
                        "💗 Refleksimu berhasil disimpan. "
                        "Data siswa diperbarui tanpa membuat "
                        "baris baru. 🌸"
                    )

            else:
                st.warning(
                    "ID siswa tidak ditemukan. Silakan isi "
                    "identitas kembali."
                )

    if st.button("🏠 Kembali ke Beranda", key="back_refleksi"):
        kembali_ke_beranda()


# =========================================================
# ROUTING
# =========================================================

if st.session_state.login_guru:

    if st.session_state.halaman == "dashboard_guru":
        halaman_dashboard_guru()

    else:
        st.session_state.halaman = "dashboard_guru"
        st.rerun()

elif st.session_state.login:

    if st.session_state.halaman == "identitas":
        halaman_identitas()

    elif st.session_state.halaman == "home":
        halaman_home()

    elif st.session_state.halaman == "materi":
        halaman_materi()

    elif st.session_state.halaman == "contoh":
        halaman_contoh()

    elif st.session_state.halaman == "tugas":
        halaman_tugas()

    elif st.session_state.halaman == "rubrik":
        halaman_rubrik()

    elif st.session_state.halaman == "refleksi":
        halaman_refleksi()

    else:
        st.session_state.halaman = "home"
        st.rerun()

else:

    if st.session_state.halaman == "login_siswa":
        halaman_login_siswa()

    elif st.session_state.halaman == "login_guru":
        halaman_login_guru()

    else:
        halaman_login()
