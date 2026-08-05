from datetime import datetime
import os
import warnings
import pandas as pd
import streamlit as st
import base64

warnings.filterwarnings('ignore')

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="CEK DATA PINJAMAN", 
    page_icon="📋",
    layout="centered"
)

# 2. Fungsi membaca gambar bg_indonesia.jpg dari GitHub sebagai Base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Panggil file bg_indonesia.jpg yang ada di repository Anda
bg_image_path = "bg_indonesia.jpg"

if os.path.exists(bg_image_path):
    encoded_bg = get_base64_of_bin_file(bg_image_path)
    bg_style = f"""
    <style>
    .stApp, [data-testid="stAppViewContainer"] {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.85)), 
                          url("data:image/jpeg;base64,{encoded_bg}") !important;
        background-size: cover !important;
        background-position: center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}
    </style>
    """
else:
    bg_style = """
    <style>
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0f172a !important;
    }
    </style>
    """

st.markdown(bg_style, unsafe_allow_html=True)

# 3. Custom CSS UI
custom_css = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* REMOVE STYLES BORDER FORM UNTUK TAMPILAN CLEAN */
    [data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    [data-testid="stStatusWidget"], .stAppDeployButton {
        transform: scale(0.75) !important;
        transform-origin: bottom right !important;
        opacity: 0.7 !important;
        transition: opacity 0.3s ease !important;
    }
    
    [data-testid="stStatusWidget"]:hover, .stAppDeployButton:hover {
        opacity: 1 !important;
    }

    /* KOTAK JUDUL UTAMA */
    .main-card {
        background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0, 180, 219, 0.3);
        margin-top: 10px;
        margin-bottom: 25px;
    }

    .header-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 6px;
        letter-spacing: 0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.15);
    }

    .header-subtitle {
        color: #e0f2fe;
        font-size: 13px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: 500;
    }

    /* TEKS & INPUT FIELD UTAMA */
    div[data-testid="stWidgetLabel"] label, p {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        letter-spacing: 0.5px !important;
    }

    div[data-baseweb="input"] {
        background-color: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
        backdrop-filter: blur(4px);
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }

    /* TOMBOL CEK DATA (FORM SUBMIT) */
    div.stButton > button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    
    div.stButton > button[kind="primaryFormSubmit"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4) !important;
    }

    /* TOMBOL BERSIHKAN */
    div.stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.1) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
        transition: all 0.2s ease !important;
        backdrop-filter: blur(4px);
    }

    div.stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
    }

    /* KARTU HASIL PENCARIAN (KOTAK PUTIH) */
    .result-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        color: #1e293b;
    }

    .result-header {
        text-align: center;
        border-bottom: 2px dashed #e2e8f0;
        padding-bottom: 15px;
        margin-bottom: 15px;
    }

    .result-header h3 a {
        display: none !important;
    }

    .result-header h3 {
        color: #0f172a !important;
        font-size: 18px;
        font-weight: 800;
        margin: 0 0 6px 0;
        letter-spacing: 1px;
        text-align: center;
    }

    /* ANIMASI GERAKAN MEMBESAR - MENGECIL (PULSING) */
    @keyframes pulseMove {
        0% {
            transform: scale(1);
            opacity: 0.85;
        }
        50% {
            transform: scale(1.12);
            opacity: 1;
        }
        100% {
            transform: scale(1);
            opacity: 0.85;
        }
    }

    /* TEKS UPDATE BERGERAK HALUS */
    .result-header p.text-update {
        color: #1e293b !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        margin: 4px 0 0 0 !important;
        letter-spacing: 1.5px !important;
        text-align: center !important;
        display: inline-block !important;
        animation: pulseMove 2.2s ease-in-out infinite !important;
    }

    .table-row {
        display: flex;
        justify-content: space-between;
        padding: 10px 0;
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
        padding: 2px 8px;
        border-radius: 6px;
        font-family: monospace;
    }

    .highlight-sisa {
        color: #dc2626;
        font-size: 16px;
        font-weight: 800;
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Nama File Excel Utama & Log
FILE_EXCEL = "DATA KOPERASI.xlsx"
FILE_LOG = "log_akses_nik.csv"

# Teks Keterangan Periode Data
TEKS_UPDATE_DATA = "PERIODE JULI 2026"


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


# Format Rupiah dengan Pembulatan Matriks
def format_rupiah(nilai):
    try:
        if not nilai or str(nilai).strip().lower() in ["nan", "none", ""]:
            return "Rp 0"
        clean_str = str(nilai).replace(",", ".").strip()
        angka = int(round(float(clean_str)))
        return f"Rp {angka:,}".replace(",", ".")
    except Exception:
        return "Rp 0" if str(nilai).strip() in ["", "nan", "None"] else str(nilai)


# Pembersihan Integer dengan Pembulatan Matriks
def clean_int(val):
    try:
        if not val or str(val).strip().lower() in ["nan", "none", ""]:
            return "0"
        clean_str = str(val).replace(",", ".").strip()
        num = float(clean_str)
        return str(int(round(num)))
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
                return val
    return ""


# Header Utama
st.markdown("""
<div class="main-card">
    <div class="header-title">📋 CEK DATA PINJAMAN KTSB MNAE</div>
    <div class="header-subtitle">🔒 Demi privasi, pastikan klik 'Tutup / Bersihkan' setelah selesai.</div>
</div>
""", unsafe_allow_html=True)

if s1 is not None:
    if "search_result" not in st.session_state:
        st.session_state["search_result"] = None

    def reset_data():
        st.session_state["nik_query"] = ""
        st.session_state["search_result"] = None

    # Penggunaan st.form secara otomatis menghapus petunjuk "Press Enter to apply"
    with st.form("form_cek_nik", clear_on_submit=False):
        nik_input = st.text_input(
            "MASUKKAN NIK KTP",
            placeholder="Ketik 16 digit NIK KTP...",
            key="nik_query",
        ).strip().replace(" ", "")

        st.write("")

        col1, col2 = st.columns(2)
        with col1:
            cek_clicked = st.form_submit_button("🔍 Cek Data", type="primary", use_container_width=True)
        with col2:
            st.form_submit_button("🔒 Tutup / Bersihkan", type="secondary", use_container_width=True, on_click=reset_data)

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
            <p class="text-update">{TEKS_UPDATE_DATA}</p>
        </div>
        <div class="table-row">
            <span class="table-label">NIK</span>
            <span class="table-value highlight-nik">{res['nik']}</span>
        </div>
        <div class="table-row">
            <span class="table-label">NAMA</span>
            <span class="table-value" style="color: #2563eb;">{res['nama']}</span>
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
elif s1 is not None and not st.session_state.get("search_result"):
    st.info("💡 Masukkan 16 digit NIK KTP lalu klik 'Cek Data' untuk melihat informasi.")