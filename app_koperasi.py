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

# 3. Custom CSS UI (Diperbarui dengan gaya Kartu Kertas Kuno / Vintage Emas)
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

    /* Styling tombol */
    .stButton button {
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0, 180, 219, 0.3) !important;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #0096c7 0%, #0077b6 100%) !important;
        border-color: #ffffff !important;
        box-shadow: 0 6px 16px rgba(0, 180, 219, 0.5) !important;
        transform: translateY(-1px) !important;
    }

    /* --- DESAIN KARTU HASIL (PERGAMUM VINTAGE GOLD) --- */
    .result-card {
        background: linear-gradient(135deg, #f7e8c4 0%, #ebd399 100%);
        border: 3px double #b38738;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6), inset 0 0 20px rgba(179, 135, 56, 0.25);
        color: #3b2a1a;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }

    .result-header {
        text-align: center;
        border-bottom: 2px solid #b38738;
        padding-bottom: 12px;
        margin-bottom: 18px;
        position: relative;
    }

    .result-header h3 {
        color: #2c1a0e !important;
        font-size: 20px;
        font-weight: 900;
        margin: 0 0 4px 0;
        text-align: center;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        font-family: 'Georgia', serif;
    }

    @keyframes pulseMove {
        0% { transform: scale(1); opacity: 0.85; }
        50% { transform: scale(1.08); opacity: 1; }
        100% { transform: scale(1); opacity: 0.85; }
    }

    .result-header p.text-update {
        color: #4a3319 !important;
        font-size: 15px !important;
        font-weight: 800 !important;
        margin: 2px 0 0 0 !important;
        text-align: center !important;
        display: inline-block !important;
        animation: pulseMove 2.2s ease-in-out infinite !important;
        letter-spacing: 0.5px;
    }

    .divider-ornament {
        text-align: center;
        color: #b38738;
        font-size: 14px;
        margin-top: -8px;
        margin-bottom: 12px;
    }

    .table-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 9px 0;
        border-bottom: 1px dashed rgba(179, 135, 56, 0.4);
        font-size: 14px;
    }

    .table-label {
        color: #594026;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .table-value {
        color: #1a0f07;
        font-weight: 800;
        text-align: right;
    }

    .highlight-nik {
        background-color: #fff8e7;
        color: #92400e;
        padding: 3px 10px;
        border-radius: 8px;
        border: 1px solid #d97706;
        font-family: monospace;
        font-size: 15px;
        letter-spacing: 0.5px;
    }

    .highlight-sisa {
        color: #b91c1c;
        font-size: 17px;
        font-weight: 900;
        background: #fee2e2;
        padding: 4px 10px;
        border-radius: 8px;
        border: 1px solid #f87171;
    }
    </style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

FILE_EXCEL = "DATA KOPERASI.xlsx"
FILE_LOG = "log_akses_nik.csv"
TEKS_UPDATE_DATA = "PERIODE OKTOBER 2026"

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
            "hutang_raw": get_val(10),        
            "hutang": format_rupiah(get_val(10)),
            "sisa_hutang_raw": get_val(3),    
            "sisa_hutang": format_rupiah(get_val(3)),
            "cicilan": format_rupiah(get_val(4)), 
            "tenor": clean_int(get_val(5)),   
            "angsuran_ke": clean_int(get_val(6)), 
            "sisa_angsuran": clean_int(get_val(7)), 
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

def reset_form_callback():
    st.session_state["search_result"] = None
    st.session_state["widget_nik_input"] = ""

if s1 is not None:
    with st.form(key="search_form"):
        nik_input = st.text_input(
            "MASUKKAN NIK KTP",
            placeholder="Ketik 16 digit NIK KTP...",
            key="widget_nik_input"
        )
        
        st.write("")
        cek_clicked = st.form_submit_button("🔍 Cek Data", type="primary", use_container_width=True)

    st.button("🔒 Tutup / Bersihkan", on_click=reset_form_callback, use_container_width=True)

    if cek_clicked:
        clean_nik = st.session_state.get("widget_nik_input", "").strip().replace(" ", "")

        if len(clean_nik) != 16 or not clean_nik.isdigit():
            st.error("❌ NIK HARUS BERISI TEPAT 16 DIGIT ANGKA!")
            st.session_state["search_result"] = None
        else:
            nama = vlookup_exact(s1, clean_nik, 2) or vlookup_exact(s4, clean_nik, 2)

            if not nama:
                st.error("❌ DATA TIDAK DITEMUKAN / NIK SALAH")
                st.session_state["search_result"] = None
            else:
                catat_log(clean_nik, nama)

                simpanan_pokok_raw = (
                    vlookup_exact(s2, clean_nik, 3)
                    or vlookup_exact(s2, clean_nik, 2)
                    or "0"
                )
                
                daftar_pinjaman = get_all_loans(s4, clean_nik)

                st.session_state["search_result"] = {
                    "nik": clean_nik,
                    "nama": nama,
                    "simpanan_pokok": format_rupiah(simpanan_pokok_raw),
                    "pinjaman_list": daftar_pinjaman
                }
        st.rerun()

# Tampilkan Hasil Pencarian
if st.session_state.get("search_result"):
    res = st.session_state["search_result"]
    pinjaman_list = res["pinjaman_list"]
    total_pinjaman_count = len(pinjaman_list)

    if total_pinjaman_count == 0:
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
        
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
            border: 1px solid #ef4444;
            border-radius: 12px;
            padding: 14px 20px;
            color: #ffffff;
            font-weight: 700;
            font-size: 15px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
            margin-bottom: 20px;
        ">
            ℹ️ Data identitas ditemukan, tidak ada catatan pinjaman aktif.
        </div>
        """, unsafe_allow_html=True)

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
        <div style="background: linear-gradient(135deg, #2a1b0e 0%, #170d06 100%); 
                    border: 2px solid #b38738; border-radius: 16px; padding: 20px; 
                    margin-bottom: 20px; text-align: center; color: white;">
            <div style="font-size: 13px; color: #d9b875; font-weight: 700; letter-spacing: 1px;">RINGKASAN ANGGOTA ({total_pinjaman_count} PINJAMAN AKTIF)</div>
            <div style="font-size: 20px; font-weight: 800; color: #f7e8c4; margin-top: 4px;">{res['nama']}</div>
            <div style="font-size: 13px; color: #e5cb96; margin-top: 2px;">SIMPANAN POKOK: <strong>{res['simpanan_pokok']}</strong></div>
            <hr style="border-color: #594026; margin: 12px 0;">
            <div style="display: flex; justify-content: space-around;">
                <div>
                    <div style="font-size: 12px; color: #e5cb96;">TOTAL CICILAN / BULAN</div>
                    <div style="font-size: 16px; font-weight: 800; color: #facc15;">{format_rupiah(total_cicilan_semua)}</div>
                </div>
                <div>
                    <div style="font-size: 12px; color: #e5cb96;">TOTAL SISA HUTANG</div>
                    <div style="font-size: 18px; font-weight: 800; color: #f87171;">{format_rupiah(total_sisa_hutang_semua)}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    for idx, pinjaman in enumerate(pinjaman_list, start=1):
        label_pinjaman = f"PINJAMAN KE-{idx}" if total_pinjaman_count > 1 else "DATA PINJAMAN ANDA"
        
        kartu_html = f"""
        <div class="result-card">
            <div class="result-header">
                <h3>{label_pinjaman}</h3>
                <div class="divider-ornament">❖ ────── ✦ ────── ❖</div>
                <p class="text-update">{TEKS_UPDATE_DATA}</p>
            </div>
            <div class="table-row">
                <span class="table-label">🪪 NIK</span>
                <span class="table-value highlight-nik">{res['nik']}</span>
            </div>
            <div class="table-row">
                <span class="table-label">👤 NAMA</span>
                <span class="table-value" style="color: #1e3a8a;">{res['nama']}</span>
            </div>
            <div class="table-row">
                <span class="table-label">🏠 SIMPANAN POKOK</span>
                <span class="table-value">{res['simpanan_pokok']}</span>
            </div>
            <div class="table-row">
                <span class="table-label">⚖️ HUTANG</span>
                <span class="table-value">{pinjaman['hutang']}</span>
            </div>
            <div class="table-row">
                <span class="table-label">📈 CICILAN PER BULAN</span>
                <span class="table-value" style="color: #065f46;">{pinjaman['cicilan']}</span>
            </div>
            <div class="table-row">
                <span class="table-label">📅 TENOR PINJAMAN</span>
                <span class="table-value">{pinjaman['tenor']} BULAN</span>
            </div>
            <div class="table-row">
                <span class="table-label">🔢 ANGSURAN KE</span>
                <span class="table-value">{pinjaman['angsuran_ke']}</span>
            </div>
            <div class="table-row">
                <span class="table-label">⏳ SISA ANGSURAN</span>
                <span class="table-value">{pinjaman['sisa_angsuran']}</span>
            </div>
            <div class="table-row" style="border-bottom: none; padding-top: 14px; margin-top: 5px;">
                <span class="table-label" style="font-size: 16px; color: #2c1a0e; font-weight: 800;">💰 SISA HUTANG</span>
                <span class="table-value highlight-sisa">{pinjaman['sisa_hutang']}</span>
            </div>
        </div>
        """
        st.markdown(kartu_html, unsafe_allow_html=True)

elif not st.session_state.get("search_result") and s1 is not None:
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #f97316 0%, #c2410c 100%);
        border: 1px solid #fb923c;
        border-radius: 12px;
        padding: 14px 20px;
        color: #ffffff;
        font-weight: 700;
        font-size: 15px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4);
        margin-bottom: 20px;
    ">
        💡 Masukkan 16 digit NIK KTP lalu klik 'Cek Data' atau tekan Enter.
    </div>
    """, unsafe_allow_html=True)