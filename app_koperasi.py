from datetime import datetime
import os
import warnings
import base64
import pandas as pd
import streamlit as st

warnings.filterwarnings('ignore')

st.set_page_config(page_title="CEK DATA PINJAMAN KTSB MNAE", layout="centered", page_icon="📋")

# Custom CSS untuk tampilan dan latar belakang
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

# Deteksi file logo secara otomatis
if os.path.exists("logo_koperasi.png"):
    FILE_LOGO = "logo_koperasi.png"
elif os.path.exists("1785240565423.png"):
    FILE_LOGO = "1785240565423.png"
else:
    FILE_LOGO = None


def get_image_base64(path):
    """Mengubah gambar menjadi format Base64 agar dapat disematkan rapi ke HTML."""
    if path and os.path.exists(path):
        with open(path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            ext = path.split(".")[-1]
            return f"data:image/{ext};base64,{encoded_string}"
    return None


@st.cache_data
def load_sheets_raw():
    try:
        excel_file = pd.ExcelFile(FILE_EXCEL, engine="openpyxl")
        s1 = pd.read_excel(excel_file, sheet_name="sheet 1", header=None, dtype=str)
        s2 = pd.read_excel(excel_file, sheet_name="sheet 2", header=None, dtype=str)
        s4 = pd.read_excel(excel_file, sheet_name="sheet 4", header=None, dtype=str)
        return s1, s2, s4
    except Exception as e:
        st.error(f"Gagal membaca file Excel. Detail: {e}")
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


if s1 is not None:
    # ------------------- POSISI LOGO DI ATAS JUDUL -------------------
    if FILE_LOGO and os.path.exists(FILE_LOGO):
        col_left, col_center, col_right = st.columns([1, 1.2, 1])
        with col_center:
            st.image(FILE_LOGO, use_container_width=True)
    
    # Judul dan Deskripsi Aplikasi
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

    # Tampilkan Kartu Hasil Pencarian
    if st.session_state["search_result"]:
        res = st.session_state["search_result"]
        
        logo_base64 = get_image_base64(FILE_LOGO)
        logo_card_html = f"<img src='{logo_base64}' style='width: 90px; margin-bottom: 10px;'><br>" if logo_base64 else ""

        st.markdown("---")
        kartu_html = f"""
        <div style='background: linear-gradient(135deg, #134e5e 0%, #71b280 100%); padding: 30px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.3); font-family: Arial, sans-serif; color: white;'>
            <div style='text-align: center; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 12px;'>
                {logo_card_html}
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