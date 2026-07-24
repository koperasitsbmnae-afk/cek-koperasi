import streamlit as st
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(page_title="CEK DATA KOPERASI", page_icon="📊", layout="centered")

# Judul Aplikasi
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>CEK DATA KOPERASI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Silakan masukkan NIK / No KTP Anda untuk melihat informasi data simpanan dan pinjaman.</p>", unsafe_allow_html=True)
st.markdown("---")

# Fungsi untuk memuat data Excel (.xlsx)
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("KOPERASI JULI 26.xlsx")
        df.columns = df.columns.astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Gagal membaca file Excel. Detail: {e}")
        return None

df = load_data()

if df is not None:
    # Cari kolom yang mengandung 'nik' atau 'ktp'
    kolom_nik = None
    for col in df.columns:
        if 'nik' in col.lower() or 'ktp' in col.lower():
            kolom_nik = col
            break

    if kolom_nik is None:
        st.error(f"⚠️ Kolom NIK/KTP tidak ditemukan di Excel. Kolom yang ada: {list(df.columns)}")
    else:
        nik_input = st.text_input("Masukan NIK / No KTP:", placeholder="Contoh: 3201234567890001")

        if st.button("Cek Data", type="primary"):
            if nik_input:
                df[kolom_nik] = df[kolom_nik].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
                hasil = df[df[kolom_nik] == str(nik_input).strip()]

                if not hasil.empty:
                    st.success("✅ Data ditemukan!")
                    row = hasil.iloc[0]
                    
                    def get_val(keys, default=0):
                        for k in keys:
                            for col in df.columns:
                                if k.lower() in col.lower():
                                    val = row.get(col, default)
                                    return val if pd.notna(val) else default
                        return default

                    nama = get_val(['nama'], '-')
                    simpanan_pokok = get_val(['simpanan pokok'], 0)
                    simpanan_wajib = get_val(['simpanan wajib'], 0)
                    simpanan_sukarela = get_val(['simpanan sukarela'], 0)
                    hutang = get_val(['hutang', 'pinjaman'], 0)
                    tenor = get_val(['tenor'], 0)
                    angsuran = get_val(['angsuran'], 0)
                    sisa_angsuran = get_val(['sisa angsuran'], 0)
                    sisa_hutang = get_val(['sisa hutang', 'sisa pinjaman'], 0)

                    kartu_html = f"""
                    <div style='background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);'>
                        <h3 style='color: #1e3a8a; border-bottom: 2px solid #cbd5e1; padding-bottom: 8px;'>Kartu Informasi Anggota</h3>
                        <table style='width: 100%; font-size: 15px; border-collapse: collapse;'>
                            <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>NO KTP / NIK</td><td style='padding: 10px; color: #2d3748;'>{nik_input}</td></tr>
                            <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>NAMA</td><td style='padding: 10px; color: #2d3748; font-weight: bold;'>{nama}</td></tr>
                            <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>SIMPANAN POKOK</td><td style='padding: 10px; color: #2d3748;'>{simpanan_pokok}</td></tr>
                            <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>SIMPANAN WAJIB</td><td style='padding: 10px; color: #2d3748;'>{simpanan_wajib}</td></tr>
                            <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>SIMPANAN SUKARELA</td><td style='padding: 10px; color: #2d3748;'>{simpanan_sukarela}</td></tr>
                            <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>HUTANG</td><td style='padding: 10px; color: #2d3748;'>{hutang}</td></tr>
                            <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>TENOR PINJAMAN</td><td style='padding: 10px; color: #2d3748;'>{tenor} BULAN</td></tr>
                            <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>ANGSURAN</td><td style='padding: 10px; color: #2d3748;'>{angsuran}</td></tr>
                            <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>SISA ANGSURAN</td><td style='padding: 10px; color: #2d3748;'>{sisa_angsuran}</td></tr>
                            <tr><td style='padding: 10px; font-weight: bold; color: #4a5568;'>SISA HUTANG</td><td style='padding: 10px; font-weight: bold; color: #e53e3e; font-size: 16px;'>{sisa_hutang}</td></tr>
                        </table>
                    </div>
                    """
                    st.markdown(kartu_html, unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Nomor KTP/NIK tidak ditemukan di dalam data koperasi. Silakan periksa kembali.")
            else:
                st.warning("⚠️ Mohon masukkan nomor KTP/NIK terlebih dahulu.")
else:
    st.info("💡 Masukkan Nomor KTP/NIK lalu klik 'Cek Data' untuk melihat informasi.")