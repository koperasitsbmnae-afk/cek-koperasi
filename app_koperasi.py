import streamlit as st

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="CEK DATA PINJAMAN KTSB MNAE",
    page_icon="📋",
    layout="centered"
)

# 2. Tampilkan Logo Koperasi di Tengah (Memanggil logo_koperasi.png yang baru dan transparan)
# Kami menggunakan trik columns untuk memusatkan gambar dengan parameter width
col1, col2, col3 = st.columns([1, 1, 1])
with col2: # Kolom tengah
    st.image("logo_koperasi.png", width=180) # Sesuaikan width jika perlu

# 3. Judul Aplikasi (Dipusatkan)
st.markdown(
    "<h1 style='text-align: center; color: white; margin-top: -30px;'>📋 CEK DATA PINJAMAN KTSB MNAE</h1>", 
    unsafe_allow_html=True
)

# 4. Pesan Privasi
st.caption("<div style='text-align: center;'>🔒 Demi privasi, pastikan klik tombol 'Tutup / Bersihkan' setelah selesai.</div>", unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True) # Jarak

# 5. Form Input NIK KTP
nik_input = st.text_input("MASUKKAN NIK KTP", placeholder="Ketik 16 digit NIK KTP...")

# 6. Tombol Aksi
col1_btn, col2_btn = st.columns(2)

with col1_btn:
    btn_cek = st.button("🔍 Cek Data", use_container_width=True)

with col2_btn:
    btn_tutup = st.button("🔒 Tutup / Bersihkan", use_container_width=True)

# 7. Logika Tombol
if btn_cek:
    if len(nik_input.strip()) == 16 and nik_input.isdigit():
        st.info(f"💡 Memproses pencarian data untuk NIK: {nik_input}...")
        # Tambahkan logika pencarian data di sini
    else:
        st.error("⚠️ Masukkan 16 digit NIK KTP yang valid!")

if btn_tutup:
    st.rerun()

# 8. Info Petunjuk Bawah
st.info("💡 Masukkan 16 digit NIK KTP lalu klik 'Cek Data' untuk melihat informasi.")