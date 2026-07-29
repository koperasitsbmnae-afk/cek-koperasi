from datetime import datetime
import os
import warnings
import pandas as pd
import streamlit as st

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="CEK DATA PINJAMAN KTSB MNAE",
    layout="centered",
    page_icon="📋"
)

# Custom CSS
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    [data-testid="stStatusWidget"], .stAppDeployButton {
        transform: scale(0.75) !important;
        transform-origin: bottom right !important;
        opacity: 0.7 !important;
        transition: opacity 0.3s ease !important;
    }
    
    [data-testid="stStatusWidget"]:hover, .stAppDeployButton:hover {
        opacity: 1 !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        background-attachment: fixed;
    }
    
    h1, h2, h3, p, label {
        color: #ffffff !important;
    }
    
    .stCaption {
        color: #d2d6dc !important;
    }

    .stButton>button {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #cbd5e0 !important;
        font-weight: bold !important;
    }
    
    .stButton>button:hover {
        background-color: #edf2f7 !important;
        color: #000000 !important;
        border-color: #a0aec0 !important;
    }
    
    .stButton>button p {
        color: #000000 !important;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

FILE_EXCEL = "KOPERASI JULI 26.xlsx"
FILE_LOG = "log_akses_nik.csv"

# Logo Koperasi Vector (Fallback Otomatis jika file png tidak ditemukan)
LOGO_SVG = """
<div style="text-align: center; margin-bottom: 10px;">
    <svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="50" cy="50" r="46" fill="#1b4d3e" stroke="#f39c12" stroke-width="3"/>
        <path d="M50 22 L53 28 L60 24 L60 31 L67 31 L64 38 L70 42 L65 47 L70 52 L65 57 L70 62 L64 66 L67 73 L60 73 L60 80 L53 76 L50 82 L47 76 L40 80 L40 73 L33 73 L36 66 L30 62 L35 57 L30 52 L35 47 L30 42 L36 38 L33 31 L40 31 L40 24 L47 28 Z" fill="#f1c40f"/>
        <circle cx="50" cy="52" r="15" fill="#1b4d3e"/>
        <path d="M50 42 L50 62 M42 48 L58 48 M42 48 L38 56 L46 56 Z M58 48 L54 56 L62 56 Z" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>
    </svg>
</div>
"""


@st.cache_data
def load_sheets_raw():
    try:
        if os.path.exists(FILE_EXCEL):
            excel_file = pd.ExcelFile(FILE_EXCEL, engine="openpyxl")
            s1 = pd.read_excel(excel_file, sheet_name="sheet 1", header=None, dtype=str)
            s2 = pd.read_excel(excel_file, sheet_name="sheet 2", header=None, dtype=str)
            s4 = pd.read_excel(excel_file, sheet_name="sheet 4", header=None, dtype=str)
            return s1, s2, s4
        else:
            st.error(f"File {FILE_EXCEL} tidak ditemukan di server GitHub.")
            return None, None, None
    except Exception as e:
        st.error(f"Gagal membaca file Excel: {e}")
        return None, None, None


s1, s2, s4 = load_sheets_raw()


def catat_log(nik, nama):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_baru = pd.DataFrame({"Waktu": [waktu], "NIK": [nik], "Nama": [nama]})
    if os.path.exists(FILE_LOG):
        data_baru.to_csv(FILE_LOG, mode="a", header=False, index=False)
    else:
        data_baru.to_csv(FILE_LOG, mode="w", header=True, index=False)


def format_rupiah(nilai):
    try:
        clean_val = str(nilai).replace(",", "").split(".")[0]
        angka = int(clean_val)
        return f"Rp {angka:,}".replace(",", ".")
    except Exception:
        return str(nilai)


def clean_int(val):
    try:
        clean_val = str(val).split(".")[0]
        return str(int(clean_val)) if clean_val and clean_val.lower() != "nan" else "0"
    except Exception:
        return "0"


def vlookup_exact(df, key, col_idx):
    if df is None or df.empty:
        return ""
    
    target_col = col_idx - 1
    mask = df.apply(lambda row: row.astype(str).str.strip().eq(key).any(), axis=1)
    matched_rows = df[mask]
    
    if not matched_rows.empty:
        row = matched_rows.iloc[0]
        if target_col < len(row):
            val = str(row.iloc[target_col]).strip()
            if val and val.lower() not in ["nan", "none"]:
                if val.endswith(".0"):
                    val = val[:-2]
                return val
    return ""


# --- PROSES RENDER TAMPILAN ---
if s1 is not None:
    # 1. Menampilkan Logo
    if os.path.exists("logo_koperasi.png"):
        c1, c2, c3 = st.columns([1, 1, 1])
        with c2:
            st.image("logo_koperasi.png", width=120)
    else:
        st.markdown(LOGO_SVG, unsafe_allow_html=True)

    # 2. Judul
    st.markdown("<h1 style='text-align: center; margin-top: -10px;'>📋 CEK DATA PINJAMAN KTSB MNAE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #d2d6dc;'>🔒 Demi privasi, pastikan klik tombol 'Tutup / Bersihkan' setelah selesai.</p>", unsafe_allow_html=True)
    st.write("")

    if "search_result" not in st.session_state:
        st.session_state["search_result"] = None

    def reset_data():
        st.session_state["nik_query"] = ""
        st.session_state["search_result"] = None

    nik_input = st.text_input(
        "MASUKAN NIK KTP",
        placeholder="Ketik 16 digit NIK KTP...",
        key="nik_query",
    ).strip()

    col1, col2 = st.columns(2)
    with col1:
        cek_clicked = st.button("🔍 Cek Data", use_container_width=True)
    with col2:
        st.button("🔒 Tutup / Bersihkan", use_container_width=True, on_click=reset_data)

    if cek_clicked:
        if len(nik_input) != 16:
            st.error("❌ NIK HARUS TEPAT 16 DIGIT!")
            st.session_state["search_result"] = None
        else:
            nama = vlookup_exact(s1, nik_input, 2)
            if not nama:
                nama = vlookup_exact(s4, nik_input, 2)

            if not nama:
                st.error("❌ DATA TIDAK DITEMUKAN / NIK SALAH")
                st.session_state["search_result"] = None
            else:
                catat_log(nik_input, nama)

                simpanan_pokok_raw = (
                    vlookup_exact(s2, nik_input, 3)
                    or vlookup_exact(s2, nik_input, 2)
                    or "0"
                )
                hutang_raw = vlookup_exact(s4, nik_input, 10) or "0"
                sisa_hutang_raw = vlookup_exact(s4, nik_input, 3) or "0"

                st.session_state["search_result"] = {
                    "nik": nik_input,
                    "nama": nama,
                    "simpanan_pokok": format_rupiah(simpanan_pokok_raw),
                    "hutang": format_rupiah(hutang_raw),
                    "sisa_hutang": format_rupiah(sisa_hutang_raw),
                    "tenor": clean_int(vlookup_exact(s4, nik_input, 5)),
                    "angsuran_ke": clean_int(vlookup_exact(s4, nik_input, 6)),
                    "sisa_angsuran": clean_int(vlookup_exact(s4, nik_input, 7)),
                }

    # Tampilkan Kartu Hasil
    if st.session_state["search_result"]:
        res = st.session_state["search_result"]

        st.markdown("---")
        kartu_html = f"""
        <div style='background: linear-gradient(135deg, #134e5e 0%, #71b280 100%); padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); font-family: Arial, sans-serif; color: white;'>
            <div style='text-align: center; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 12px;'>
                <h3 style='margin: 0; font-size: 20px; letter-spacing: 2px; text-transform: uppercase; color: #ffffff;'>DATA PINJAMAN ANDA</h3>
                <p style='margin: 5px 0 0 0; font-size: 12px; color: #e2e8f0; letter-spacing: 1px;'>KTSB MNAE UPDATE JUNI 2026</p>
            </div>
            <div style='background-color: rgba(255, 255, 255, 0.95); padding: 20px; border-radius: 10px; color: #333;'>
                <table style='width:100%; border-collapse: collapse; font-size: 15px;'>
                    <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; width: 40%; color: #4a5568;'>NIK</td><td style='padding: 10px; background-color: #fff3cd; font-weight: bold; color: #856404; border-radius: 4px;'>{res['nik']}</td></tr>
                    <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>NAMA</td><td style='padding: 10px; font-weight: bold; color: #2b6cb0;'>{res['nama']}</td></tr>
                    <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>SIMPANAN POKOK</td><td style='padding: 10px; color: #2d3748;'>{res['simpanan_pokok']}</td></tr>
                    <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>HUTANG</td><td style='padding: 10px; color: #2d3748;'>{res['hutang']}</td></tr>
                    <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>TENOR PINJAMAN</td><td style='padding: 10px; color: #2d3748;'>{res['tenor']} BULAN</td></tr>
                    <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>ANGSURAN KE</td><td style='padding: 10px; color: #2d3748;'>{res['angsuran_ke']}</td></tr>
                    <tr style='border-bottom: 1px solid #edf2f7;'><td style='padding: 10px; font-weight: bold; color: #4a5568;'>SISA ANGSURAN</td><td style='padding: 10px; color: #2d3748;'>{res['sisa_angsuran']}</td></tr>
                    <tr><td style='padding: 10px; font-weight: bold; color: #4a5568;'>SISA HUTANG</td><td style='padding: 10px; font-weight: bold; color: #e53e3e; font-size: 16px;'>{res['sisa_hutang']}</td></tr>
                </table>
            </div>
        </div>
        """
        st.markdown(kartu_html, unsafe_allow_html=True)
    elif not cek_clicked:
        st.info("💡 Masukkan 16 digit NIK KTP lalu klik 'Cek Data' untuk melihat informasi.")