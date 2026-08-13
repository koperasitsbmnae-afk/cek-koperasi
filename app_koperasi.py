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
    
    div[data-testid="stInputInstruction"],
    div[data-testid="stInputInstruction"] *,
    div[data-testid="stTextInput"] div[data-testid="stInputInstruction"],
    div[data-baseweb="input"] + div,
    .stTextInput small,
    [data-testid="stTextInput"] small {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        position: absolute !important;
        pointer-events: none !important;
    }
    
    [data-testid="stStatusWidget"], .stAppDeployButton {
        transform: scale(0.75) !important;
        transform-origin: bottom right !important;
        opacity: 0.7 !important;
        transition: opacity 0.3s ease !important;
    }

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

    div[data-testid="stWidgetLabel"] label, p {
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    div[data-baseweb="input"] {
        background-color: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }

    /* CSS Tombol Tutup/Bersihkan (Biru Langit Gradient) */
    div[data-testid="stFormSubmitButton"] button[kind="secondaryFormSubmit"],
    button[data-testid="baseButton-secondaryFormSubmit"],
    button[kind="secondary"] {
        background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 180, 219, 0.3) !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="stFormSubmitButton"] button[kind="secondaryFormSubmit"]:hover,
    button[data-testid="baseButton-secondaryFormSubmit"]:hover,
    button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #0096c7 0%, #0077b6 100%) !important;
        border-color: #ffffff !important;
        box-shadow: 0 6px 16px rgba(0, 180, 219, 0.5) !important;
        transform: translateY(-1px) !important;
    }

    .result-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        color: #1e293b;
        margin-bottom: 20px;
    }

    .result-header {
        text-align: center;
        border-bottom: 2px dashed #e2e8f0;
        padding-bottom: 15px;
        margin-bottom: 15px;
    }

    .result-header h3 {
        color: #0f172a !important;
        font-size: 18px;
        font-weight: 800;
        margin: 0 0 6px 0;
        text-align: center;
    }

    @keyframes pulseMove {
        0% { transform: scale(1); opacity: 0.85; }
        50% { transform: scale(1.12); opacity: 1; }
        100% { transform: scale(1); opacity: 0.85; }
    }

    .result-header p.text-update {
        color: #1e293b !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        margin: 4px 0 0 0 !important;
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

    .table-label { color: #64748b; font-weight: 600; }
    .table-value { color: #0f172a; font-weight: 700; text-align: right; }
    .highlight-nik {
        background-color: #fef3c7;
        color: #92400e;
        padding: 2px 8px;
        border-radius: 6px;
        font-family: monospace;
    }
    .highlight-sisa { color: #dc2626; font-size: 16px; font-weight: 800; }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

FILE_EXCEL = "DATA KOPERASI.xlsx"
FILE_LOG = "log_akses_nik.csv"
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

def format_rupiah(nilai):
    try:
        if not nilai or str(nilai).strip().lower() in ["nan", "none", ""]:
            return "Rp 0"
        clean_str = str(nilai).replace(",", ".").strip()
        angka = int(round(float(clean_str)))
        return f"Rp {angka:,}".replace(",", ".")
    except Exception:
        return "Rp 0" if str(nilai).strip() in ["", "nan", "None"] else str(nilai)

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
    matched_rows = df[df[0].astype(str).str.strip() == key]
    if not matched_rows.empty:
        row = matched_rows.iloc[0]
        if target_col < len(row):
            val = str(row.iloc[target_col]).strip()
            if val and val.lower() not in ["nan", "none"]:
                return val
    return ""

def get_all_loans(df_s4, key):
    if df_s4 is None or df_s4.empty:
        return []
    
    matched_rows = df_s4[df_s4[0].astype(str).str.strip() == key]
    loans = []
    for _, row in matched_rows.iterrows():
        def get_val(col_idx):
            target = col_idx - 1
            if target < len(row):
                v = str(row.iloc[target]).strip()
                if v and v.lower() not in ["nan", "none"]:
                    return v
            return "0"

        loans.append({
            "hutang_raw": get_val(10),        # Kolom J: PINJAMAN POKOK
            "hutang": format_rupiah(get_val(10)),
            "sisa_hutang_raw": get_val(3),    # Kolom C: SISA HUTANG
            "sisa_hutang": format_rupiah(get_val(3)),
            "cicilan": format_rupiah(get_val(4)), # Kolom D: CICILAN PER BULAN
            "tenor": clean_int(get_val(5)),   # Kolom E: TENOR
            "angsuran_ke": clean_int(get_val(6)), # Kolom F: ANGSURAN KE
            "sisa_angsuran": clean_int(get_val(7)), # Kolom G: SISA ANGSURAN
        })
    return loans

# Header Utama
st.markdown("""
<div class="main-card">
    <div class="header-title">📋 CEK DATA PINJAMAN KTSB MNAE</div>
    <div class="header-subtitle">🔒 Demi privasi, pastikan klik 'Tutup / Bersihkan' setelah selesai.</div>
</div>
""", unsafe_allow_html=True)

if "search_result" not in st.session_state:
    st.session_state["search_result"] = None

if s1 is not None:
    with st.form(key="search_form"):
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
            reset_clicked = st.form_submit_button("🔒 Tutup / Bersihkan", type="secondary", use_container_width=True)

    if reset_clicked:
        st.session_state["search_result"] = None
        st.rerun()

    if cek_clicked:
        if len(nik_input) != 16 or not nik_input.isdigit():
            st.error("❌ NIK HARUS BERISI TEPAT 16 DIGIT ANGKA!")
            st.session_state["search_result"] = None
        else:
            nama = vlookup_exact(s1, nik_input, 2) or vlookup_exact(s4, nik_input, 2)

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
                
                daftar_pinjaman = get_all_loans(s4, nik_input)

                st.session_state["search_result"] = {
                    "nik": nik_input,
                    "nama": nama,
                    "simpanan_pokok": format_rupiah(simpanan_pokok_raw),
                    "pinjaman_list": daftar_pinjaman
                }

# Tampilkan Hasil Pencarian
if st.session_state.get("search_result"):
    res = st.session_state["search_result"]
    pinjaman_list = res["pinjaman_list"]
    total_pinjaman_count = len(pinjaman_list)

    if total_pinjaman_count == 0:
        # Jika tidak ada pinjaman aktif, buat data default agar kartu tetap tampil
        pinjaman_list = [{
            "hutang": "Rp 0",
            "sisa_hutang_raw": "0",
            "sisa_hutang": "Rp 0",
            "cicilan": "Rp 0",
            "tenor": "-",
            "angsuran_ke": "-",
            "sisa_angsuran": "-"
        }]
        total_pinjaman_count = 1
        st.info("ℹ️ Data identitas ditemukan, tidak ada catatan pinjaman aktif.")

    # Ringkasan Total Multi-Pinjaman (hanya jika > 1 pinjaman)
    if total_pinjaman_count > 1:
        total_sisa_hutang_semua = 0
        total_cicilan_semua = 0
        for p in pinjaman_list:
            try:
                total_sisa_hutang_semua += int(round(float(p['sisa_hutang_raw'].replace(",", "."))))
            except:
                pass
            try:
                cicilan_clean = p['cicilan'].replace("Rp", "").replace(".", "").strip()
                total_cicilan_semua += int(cicilan_clean)
            except:
                pass
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); 
                    border: 2px solid #3b82f6; border-radius: 16px; padding: 20px; 
                    margin-bottom: 20px; text-align: center; color: white;">
            <div style="font-size: 13px; color: #94a3b8; font-weight: 700; letter-spacing: 1px;">RINGKASAN ANGGOTA ({total_pinjaman_count} PINJAMAN AKTIF)</div>
            <div style="font-size: 20px; font-weight: 800; color: #60a5fa; margin-top: 4px;">{res['nama']}</div>
            <div style="font-size: 13px; color: #cbd5e1; margin-top: 2px;">SIMPANAN POKOK: <strong>{res['simpanan_pokok']}</strong></div>
            <hr style="border-color: #334155; margin: 12px 0;">
            <div style="display: flex; justify-content: space-around;">
                <div>
                    <div style="font-size: 12px; color: #cbd5e1;">TOTAL CICILAN / BULAN</div>
                    <div style="font-size: 16px; font-weight: 800; color: #facc15;">{format_rupiah(total_cicilan_semua)}</div>
                </div>
                <div>
                    <div style="font-size: 12px; color: #cbd5e1;">TOTAL SISA HUTANG</div>
                    <div style="font-size: 18px; font-weight: 800; color: #ef4444;">{format_rupiah(total_sisa_hutang_semua)}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Kartu Detail Pinjaman
    for idx, pinjaman in enumerate(pinjaman_list, start=1):
        label_pinjaman = f"PINJAMAN KE-{idx}" if total_pinjaman_count > 1 else "DATA PINJAMAN ANDA"
        
        kartu_html = f"""
        <div class="result-card">
            <div class="result-header">
                <h3>{label_pinjaman}</h3>
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
                <span class="table-value">{pinjaman['hutang']}</span>
            </div>
            <div class="table-row">
                <span class="table-label">CICILAN PER BULAN</span>
                <span class="table-value" style="color: #059669;">{pinjaman['cicilan']}</span>
            </div>
            <div class="table-row">
                <span class="table-label">TENOR PINJAMAN</span>
                <span class="table-value">{pinjaman['tenor']} BULAN</span>
            </div>
            <div class="table-row">
                <span class="table-label">ANGSURAN KE</span>
                <span class="table-value">{pinjaman['angsuran_ke']}</span>
            </div>
            <div class="table-row">
                <span class="table-label">SISA ANGSURAN</span>
                <span class="table-value">{pinjaman['sisa_angsuran']}</span>
            </div>
            <div class="table-row" style="border-bottom: none; padding-top: 15px;">
                <span class="table-label" style="font-size: 16px; color: #0f172a;">SISA HUTANG</span>
                <span class="table-value highlight-sisa">{pinjaman['sisa_hutang']}</span>
            </div>
        </div>
        """
        st.markdown(kartu_html, unsafe_allow_html=True)

elif not st.session_state.get("search_result") and s1 is not None:
    st.info("💡 Masukkan 16 digit NIK KTP lalu klik 'Cek Data' atau tekan Enter.")