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

# 2. Fungsi membaca gambar bg_indonesia.jpg sebagai Base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

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
    .main-card {
        background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0, 180, 219, 0.3);
        margin-top: 10px;
        margin-bottom: 25px;
    }
    .header-title { color: #ffffff; font-size: 22px; font-weight: 800; text-align: center; margin-bottom: 6px; }
    .header-subtitle { color: #e0f2fe; font-size: 13px; text-align: center; margin-bottom: 20px; }
    .result-card { background: #ffffff; border-radius: 16px; padding: 24px; box-shadow: 0 15px 35px rgba(0,0,0,0.4); color: #1e293b; margin-bottom: 20px; }
    .result-header { text-align: center; border-bottom: 2px dashed #e2e8f0; padding-bottom: 15px; margin-bottom: 15px; }
    .table-row { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #f1f5f9; }
    .table-label { color: #64748b; font-weight: 600; }
    .table-value { color: #0f172a; font-weight: 700; text-align: right; }
    .highlight-nik { background-color: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 6px; font-family: monospace; }
    .highlight-sisa { color: #dc2626; font-size: 16px; font-weight: 800; }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- FUNGSI UTAMA ---
FILE_EXCEL = "DATA KOPERASI.xlsx"
TEKS_UPDATE_DATA = "PERIODE JULI 2026"

@st.cache_data(ttl=60)
def load_sheets_raw():
    try:
        excel_file = pd.ExcelFile(FILE_EXCEL, engine="openpyxl")
        return pd.read_excel(excel_file, sheet_name="sheet 1", header=None, dtype=str), \
               pd.read_excel(excel_file, sheet_name="sheet 2", header=None, dtype=str), \
               pd.read_excel(excel_file, sheet_name="sheet 4", header=None, dtype=str)
    except: return None, None, None

s1, s2, s4 = load_sheets_raw()

def format_rupiah(nilai):
    try:
        if not nilai or str(nilai).strip().lower() in ["nan", "none", ""]: return "Rp 0"
        return f"Rp {int(round(float(str(nilai).replace(',', '.')))):,}".replace(",", ".")
    except: return "Rp 0"

def vlookup_exact(df, key, col_idx):
    if df is None or df.empty: return ""
    matched = df[df[0].astype(str).str.strip() == key]
    if not matched.empty:
        val = str(matched.iloc[0, col_idx-1]).strip()
        return val if val.lower() not in ["nan", "none"] else ""
    return ""

def get_all_loans(df, key):
    matched = df[df[0].astype(str).str.strip() == key]
    loans = []
    for _, row in matched.iterrows():
        loans.append({
            "hutang": format_rupiah(row.iloc[9]),
            "sisa_hutang": format_rupiah(row.iloc[2]),
            "sisa_hutang_raw": str(row.iloc[2]) if str(row.iloc[2]) not in ["nan", "None"] else "0",
            "cicilan": format_rupiah(row.iloc[3]),
            "tenor": str(row.iloc[4]),
            "angsuran_ke": str(row.iloc[5]),
            "sisa_angsuran": str(row.iloc[6])
        })
    return loans

# --- UI APP ---
st.markdown('<div class="main-card"><div class="header-title">📋 CEK DATA PINJAMAN KTSB MNAE</div><div class="header-subtitle">🔒 Demi privasi, pastikan klik \'Tutup / Bersihkan\' setelah selesai.</div></div>', unsafe_allow_html=True)

if "search_result" not in st.session_state: st.session_state["search_result"] = None

with st.form(key="search_form"):
    nik_input = st.text_input("MASUKKAN NIK KTP", placeholder="Ketik 16 digit NIK...")
    col1, col2 = st.columns(2)
    cek = col1.form_submit_button("🔍 Cek Data", type="primary", use_container_width=True)
    reset = col2.form_submit_button("🔒 Tutup / Bersihkan", use_container_width=True)

if reset:
    st.session_state["search_result"] = None
    st.rerun()

if cek:
    nik_clean = "".join(filter(str.isdigit, nik_input))
    if len(nik_clean) != 16:
        st.error("❌ NIK HARUS BERISI TEPAT 16 DIGIT ANGKA!")
    else:
        nama = vlookup_exact(s1, nik_clean, 2) or vlookup_exact(s4, nik_clean, 2)
        if not nama:
            st.error("❌ DATA TIDAK DITEMUKAN")
        else:
            simpanan = format_rupiah(vlookup_exact(s2, nik_clean, 3) or vlookup_exact(s2, nik_clean, 2) or "0")
            st.session_state["search_result"] = {"nik": nik_clean, "nama": nama, "simpanan": simpanan, "loans": get_all_loans(s4, nik_clean)}

# --- HASIL ---
if st.session_state["search_result"]:
    res = st.session_state["search_result"]
    loans = res["loans"] if len(res["loans"]) > 0 else [{"hutang":"Rp 0","sisa_hutang":"Rp 0","sisa_hutang_raw":"0","cicilan":"Rp 0","tenor":"-","angsuran_ke":"-","sisa_angsuran":"-"}]
    
    for p in loans:
        st.markdown(f'''
        <div class="result-card">
            <div class="result-header"><h3>DATA PINJAMAN ANDA</h3><p>{TEKS_UPDATE_DATA}</p></div>
            <div class="table-row"><span class="table-label">NIK</span><span class="table-value highlight-nik">{res['nik']}</span></div>
            <div class="table-row"><span class="table-label">NAMA</span><span class="table-value">{res['nama']}</span></div>
            <div class="table-row"><span class="table-label">SIMPANAN POKOK</span><span class="table-value">{res['simpanan']}</span></div>
            <div class="table-row"><span class="table-label">HUTANG</span><span class="table-value">{p['hutang']}</span></div>
            <div class="table-row"><span class="table-label">CICILAN</span><span class="table-value">{p['cicilan']}</span></div>
            <div class="table-row"><span class="table-label">TENOR</span><span class="table-value">{p['tenor']} BULAN</span></div>
            <div class="table-row"><span class="table-label">ANGSURAN KE</span><span class="table-value">{p['angsuran_ke']}</span></div>
            <div class="table-row" style="border:none;"><span class="table-label">SISA HUTANG</span><span class="table-value highlight-sisa">{p['sisa_hutang']}</span></div>
        </div>
        ''', unsafe_allow_html=True)