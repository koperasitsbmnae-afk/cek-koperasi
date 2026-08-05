from datetime import datetime
import os
import warnings
import pandas as pd
import streamlit as st

warnings.filterwarnings('ignore')

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="CEK DATA PINJAMAN", 
    page_icon="📋",
    layout="centered"
)

# 2. Custom CSS UI Modern, Glassmorphism & Background Keuangan Elegan
custom_css = """
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

    /* BACKGROUND TEMA KEUANGAN & KOPERASI MODERN (NON-CANDLESTICK) */
    .stApp {
        background: linear-gradient(rgba(10, 25, 47, 0.82), rgba(15, 23, 42, 0.90)), 
                    url('https://images.unsplash.com/photo-1559526324-4b87b5e36e44?q=80&w=1920&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* KOTAK JUDUL UTAMA - GRADASI TEAL/BLUE DENGAN EFEK GLOW */
    .main-card {
        background: linear-gradient(135deg, #0284c7 0%, #0d9488 100%);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 12px 35px rgba(13, 148, 136, 0.35);
        margin-top: 10px;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }

    .header-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 6px;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    .header-subtitle {
        color: #f0fdf4;
        font-size: 13px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: 500;
    }

    /* LABELS & INPUT FIELD */
    div[data-testid="stWidgetLabel"] label, p {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        letter-spacing: 0.5px !important;
    }

    div[data-baseweb="input"] {
        background-color: rgba(15, 23, 42, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        backdrop-filter: blur(8px);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #14b8a6 !important;
        box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.3) !important;
    }

    /* TOMBOL CEK DATA */
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #0d9488 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 12px 18px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 18px rgba(13, 148, 136, 0.4) !important;
    }
    
    div.stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(13, 148, 136, 0.5) !important;
    }

    /* TOMBOL BERSIHKAN */
    div.stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.12) !important;
        color: #e2e8f0 !important;
        border: 1px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 12px 18px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(8px);
    }

    div.stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.22) !important;
        color: #ffffff !important;
    }

    /* KARTU HASIL PENCARIAN (GLASSMORPHISM WHITE CARD) */
    .result-card {
        background: rgba(255, 255, 255, 0.96);
        border-radius: 20px;
        padding: 26px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        color: #0f172a;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.8);
    }

    .result-header {
        text-align: center;
        border-bottom: 2px dashed #cbd5e1;
        padding-bottom: 15px;
        margin-bottom: 15px;
    }

    .result-header h3 {
        color: #0f172a !important;
        font-size: 19px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 1px;
    }

    .result-header p {
        color: #64748b !important;
        font-size: 11px !important;
        margin: 4px 0 0 0;
        font-weight: 600 !important;
    }

    .table-row {
        display: flex;
        justify-content: space-between;
        padding: 11px 0;
        border-bottom: 1px solid #f1f5f9;
        font-size: 14px;
    }

    .table-label {
        color: #64748b;
        font-weight: 600;
    }

    .table-value {
        color: #0f172a;
        font-weight: 700;
        text-align: right;
    }

    .highlight-nik {
        background-color: #fef3c7;
        color: #92400e;
        padding: 3px 10px;
        border-radius: 6px;
        font-family: monospace;
        font-weight: 800;
    }

    .highlight-sisa {
        color: #dc2626;
        font-size: 17px;
        font-weight: 800;
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Nama File Excel Utama & Log
FILE_EXCEL = "DATA KOPERASI.xlsx"
FILE_LOG = "log_akses_nik.csv"

# Teks Keterangan Update Data
TEKS_UPDATE_DATA = "KTSB MNAE UPDATE JULI 2026"


@st.cache_data(ttl=60)
def load_sheets_raw():
    try:
        excel_file = pd.ExcelFile(FILE_EXCEL, engine="openpyxl")
        s1 = pd.read_excel(excel_file, sheet_name="sheet 1", header=None, dtype=str)
        s2 = pd.read_excel(excel_file, sheet_name="sheet 2", header=None, dtype=str)
        s4 = pd.read_excel(excel_file, sheet_name="sheet 4", header=None, dtype=str)
        return s1, s2, s4
    except Exception as e:
        st.error(f"Gagal membaca file Excel '{FILE_EXCEL}'. Detail Error: {e}")
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
        return "Rp 0" if str(nilai).strip() in ["", "nan", "None"] else str(nilai)


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


# Header Utama UI
st.markdown("""
<div class="main-card">
    <div class="header-title">📋 CEK DATA PINJAMAN KTSB MNAE</div>
    <div class="header-subtitle">🔒 Demi privasi, pastikan klik 'Tutup / Bersihkan' setelah selesai.</div>
</div>
""", unsafe_allow_html=True)

# Inisialisasi variabel default
cek_clicked = False

if s1 is not None:
    if "search_result" not in st.session_state:
        st.session_state["search_result"] = None

    def reset_data():
        st.session_state["nik_query"] = ""
        st.session_state["search_result"] = None

    nik_input = st.text_input(
        "MASUKKAN NIK KTP",
        placeholder="Ketik 16 digit NIK KTP...",
        key="nik_query",
    ).strip().replace(" ", "")

    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        cek_clicked = st.button("🔍 Cek Data", type="primary", use_container_width=True)
    with col2:
        st.button("🔒 Tutup / Bersihkan", type="secondary", use_container_width=True, on_click=reset_data)

    if cek_clicked:
        if len(nik_input) != 16 or not nik_input.isdigit():
            st.error("❌ NIK HARUS BERISI TEPAT 16 DIGIT ANGKA!")
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
if st.session_state.get("search_result"):
    res = st.session_state["search_result"]
    kartu_html = f"""
    <div class="result-card">
        <div class="result-header">
            <h3>DATA PINJAMAN ANDA</h3>
            <p>{TEKS_UPDATE_DATA}</p>
        </div>
        <div class="table-row">
            <span class="table-label">NIK</span>
            <span class="table-value highlight-nik">{res['nik']}</span>
        </div>
        <div class="table-row">
            <span class="table-label">NAMA</span>
            <span class="table-value" style="color: #0284c7;">{res['nama']}</span>
        </div>
        <div class="table-row">
            <span class="table-label">SIMPANAN POKOK</span>
            <span class="table-value">{res['simpanan_pokok']}</span>
        </div>
        <div class="table-row">
            <span class="table-label">HUTANG</span>
            <span class="table-value">{res['hutang']}</span>
        </div>
        <div class="table-row">
            <span class="table-label">TENOR PINJAMAN</span>
            <span class="table-value">{res['tenor']} BULAN</span>
        </div>
        <div class="table-row">
            <span class="table-label">ANGSURAN KE</span>
            <span class="table-value">{res['angsuran_ke']}</span>
        </div>
        <div class="table-row">
            <span class="table-label">SISA ANGSURAN</span>
            <span class="table-value">{res['sisa_angsuran']}</span>
        </div>
        <div class="table-row" style="border-bottom: none; padding-top: 15px;">
            <span class="table-label" style="font-size: 16px; color: #0f172a;">SISA HUTANG</span>
            <span class="table-value highlight-sisa">{res['sisa_hutang']}</span>
        </div>
    </div>
    """
    st.markdown(kartu_html, unsafe_allow_html=True)
elif not cek_clicked and s1 is not None:
    st.info("💡 Masukkan 16 digit NIK KTP lalu klik 'Cek Data' untuk melihat informasi.")