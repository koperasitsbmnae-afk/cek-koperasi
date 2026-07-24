import streamlit as st
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(page_title="CEK DATA KOPERASI", page_icon="📊", layout="centered")

# Judul Aplikasi
st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>CEK DATA KOPERASI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Silakan masukkan NIK Anda untuk melihat informasi data simpanan dan pinjaman.</p>", unsafe_allow_html=True)
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
    nik_input = st.text_input("Masukan NIK KTP:", placeholder="Contoh: 3201234567890001")

    if st.button("Cek Data", type="primary"):
        if nik_input:
            df['NIK'] = df['NIK'].astype(str).str.strip()
            hasil = df[df['NIK'] == str(nik_input).strip()]

            if not hasil.empty:
                st.success("✅ Data ditemukan!")
                row = hasil.iloc[0]
                
                nama = row.get('NAMA', '-')
                simpanan_pokok = row.get('SIMPANAN POKOK', 0)
                simpanan_wajib = row.get('SIMPANAN WAJIB', 0)
                simpanan_sukarela = row.get('SIMPANAN SUKARELA', 0)
                hutang = row.get('HUTANG', 0)
                tenor = row.get('TENOR', 0)
                angsuran = row.get('ANGSURAN', 0)
                sisa_angsuran = row.get('SISA ANGSURAN', 0)
                sisa_hutang = row.get('SISA HUTANG', 0)

                kartu_html = f"""
                <div style='background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);'>
                    <h3 style='color: #1e3a8a; border-bottom: 2px solid #cbd5e1; padding-bottom: 8px;'>Kartu Informasi Anggota</h3>
                    <table style='width: 100%; font-size: 15px; border-collapse: collapse;'>
                        <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>NIK</td><td style='padding: 10px; color: #2d3748;'>{nik_input}</td></tr>
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
                st.warning("⚠️ NIK tidak ditemukan di dalam data koperasi. Silakan periksa kembali.")
        else:
            st.warning("⚠️ Mohon masukkan nomor NIK terlebih dahulu.")
else:
    st.info("💡 Masukkan NIK KTP lalu klik 'Cek Data' untuk melihat informasi.")