from datetime import datetime
import os
import warnings
import pandas as pd
import streamlit as st

warnings.filterwarnings('ignore')

st.set_page_config(page_title="CEK DATA KOPERASI", layout="centered")

# Sembunyikan header, menu, dan footer bawaan Streamlit
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

FILE_EXCEL = "KOPERASI JULI 26.xlsx"
FILE_LOG = "log_akses_nik.csv"


@st.cache_data
def load_sheets_raw():
    try:
        excel_file = pd.ExcelFile(FILE_EXCEL, engine="openpyxl")
        s1 = pd.read_excel(excel_file, sheet_name="sheet 1", header=None)
        s2 = pd.read_excel(excel_file, sheet_name="sheet 2", header=None)
        s4 = pd.read_excel(excel_file, sheet_name="sheet 4", header=None)
        return s1, s2, s4
    except Exception as e:
        st.error(f"Gagal membaca file Excel. Detail: {e}")
        return None, None, None


s1, s2, s4 = load_sheets_raw()


# Fungsi untuk mencatat log akses ke file CSV
def catat_log(nik, nama):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_baru = pd.DataFrame({"Waktu": [waktu], "NIK": [nik], "Nama": [nama]})
    if os.path.exists(FILE_LOG):
        data_baru.to_csv(FILE_LOG, mode="a", header=False, index=False)
    else:
        data_baru.to_csv(FILE_LOG, mode="w", header=True, index=False)


# Fungsi untuk memformat angka menjadi Rupiah
def format_rupiah(nilai):
    try:
        clean_val = str(nilai).replace(",", "").split(".")[0]
        angka = int(clean_val)
        return f"Rp {angka:,}".replace(",", ".")
    except:
        return nilai


# Fungsi untuk membersihkan nilai numerik (Tenor, Angsuran, dll) agar bulat rapi
def clean_int(val):
    try:
        clean_val = str(val).split(".")[0]
        return str(int(clean_val)) if clean_val and clean_val.lower() != "nan" else "0"
    except:
        return "0"


if s1 is not None:
    # Sidebar untuk Pilihan Menu (Menu Utama vs Menu Admin)
    st.sidebar.title("📌 Navigasi")
    pilihan_menu = st.sidebar.radio(
        "Pilih Menu:", ["Cek Data Anggota", "Riwayat Akses Admin"]
    )

    if pilihan_menu == "Cek Data Anggota":
        st.title("📋 CEK DATA ANGGOTA")
        st.caption(
            "🔒 Demi privasi, pastikan klik tombol 'Tutup / Bersihkan' setelah"
            " selesai."
        )

        if "nik_query" not in st.session_state:
            st.session_state["nik_query"] = ""


        def reset_data():
            st.session_state["nik_query"] = ""


        nik_input = st.text_input(
            "MASUKAN NIK KTP",
            placeholder="Ketik 16 digit NIK KTP...",
            key="nik_query",
        ).strip()

        col1, col2 = st.columns(2)
        with col1:
            cek_clicked = st.button("🔍 Cek Data", use_container_width=True)
        with col2:
            st.button(
                "🔒 Tutup / Bersihkan",
                use_container_width=True,
                on_click=reset_data,
            )

        if cek_clicked and nik_input:
            if len(nik_input) != 16:
                st.error("❌ NIK HARUS TEPAT 16 DIGIT!")
            else:

                def vlookup_exact(df, key, col_idx):
                    if df is None or df.empty:
                        return ""
                    target_col = col_idx - 1
                    for _, row in df.iterrows():
                        row_str = [str(val).strip() for val in row.values]
                        if any(key == item for item in row_str):
                            if target_col < len(row):
                                val = str(row.iloc[target_col]).strip()
                                if (
                                    val
                                    and val.lower() != "nan"
                                    and val.lower() != "none"
                                ):
                                    if val.endswith(".0"):
                                        val = val[:-2]
                                    return val
                    return ""


                nama = vlookup_exact(s1, nik_input, 2)
                if not nama:
                    nama = vlookup_exact(s4, nik_input, 2)

                if not nama:
                    st.error("❌ DATA TIDAK DITEMUKAN / NIK SALAH")
                else:
                    # Catat otomatis ke log riwayat
                    catat_log(nik_input, nama)

                    simpanan_pokok_raw = (
                        vlookup_exact(s2, nik_input, 3)
                        or vlookup_exact(s2, nik_input, 2)
                        or "0"
                    )
                    hutang_raw = vlookup_exact(s4, nik_input, 10) or "0"
                    sisa_hutang_raw = vlookup_exact(s4, nik_input, 3) or "0"

                    simpanan_pokok = format_rupiah(simpanan_pokok_raw)
                    hutang = format_rupiah(hutang_raw)
                    sisa_hutang = format_rupiah(sisa_hutang_raw)

                    # Menggunakan clean_int agar tidak ada desimal panjang
                    tenor = clean_int(vlookup_exact(s4, nik_input, 5))
                    angsuran_ke = clean_int(vlookup_exact(s4, nik_input, 6))
                    sisa_angsuran = clean_int(vlookup_exact(s4, nik_input, 7))

                    st.markdown("---")

                    kartu_html = (
                        "<div style='background: linear-gradient(135deg,"
                        " #0f2027 0%, #203a43 50%, #2c5364 100%); padding:"
                        " 30px; border-radius: 16px; box-shadow: 0 10px 25px"
                        " rgba(0,0,0,0.2); font-family: Arial, sans-serif;"
                        " color: white;'><div style='text-align: center;"
                        " margin-bottom: 20px; border-bottom: 1px solid"
                        " rgba(255,255,255,0.2); padding-bottom: 12px;'><h3"
                        " style='margin: 0; font-size: 20px; letter-spacing:"
                        " 2px; text-transform: uppercase; color:"
                        " #ffffff;'>KARTU INFORMASI ANGGOTA</h3><p"
                        " style='margin: 5px 0 0 0; font-size: 12px; color:"
                        " #a0aec0; letter-spacing: 1px;'>KTSB MNAE UPDATE JUNI"
                        " 2026</p></div><div style='background-color: rgba(255,"
                        " 255, 255, 0.95); padding: 20px; border-radius: 10px;"
                        " color: #333;'><table style='width:100%; border-collapse:"
                        f" collapse; font-size: 15px;'><tr style='border-bottom:"
                        " 1px solid #edf2f7;'><td style='padding: 10px;"
                        f" font-weight: bold; width: 40%; color:"
                        f" #4a5568;'>NIK</td><td style='padding: 10px;"
                        " background-color: #fff3cd; font-weight: bold; color:"
                        f" #856404; border-radius: 4px;'>{nik_input}</td></tr><tr"
                        " style='border-bottom: 1px solid #edf2f7;'><td"
                        " style='padding: 10px; font-weight: bold; color:"
                        f" #4a5568;'>NAMA</td><td style='padding: 10px;"
                        f" font-weight: bold; color: #2b6cb0;'>{nama}</td></tr><tr"
                        " style='border-bottom: 1px solid #edf2f7;'><td"
                        " style='padding: 10px; font-weight: bold; color:"
                        f" #4a5568;'>SIMPANAN POKOK</td><td style='padding: 10px;"
                        f" color: #2d3748;'>{simpanan_pokok}</td></tr><tr"
                        " style='border-bottom: 1px solid #edf2f7;'><td"
                        " style='padding: 10px; font-weight: bold; color:"
                        f" #4a5568;'>HUTANG</td><td style='padding: 10px; color:"
                        f" #2d3748;'>{hutang}</td></tr><tr style='border-bottom:"
                        " 1px solid #edf2f7;'><td style='padding: 10px;"
                        f" font-weight: bold; color: #4a5568;'>TENOR PINJAMAN</td><td"
                        f" style='padding: 10px; color: #2d3748;'>{tenor}"
                        " BULAN</td></tr><tr style='border-bottom: 1px solid"
                        " #edf2f7;'><td style='padding: 10px; font-weight: bold;"
                        f" color: #4a5568;'>ANGSURAN KE</td><td style='padding:"
                        f" 10px; color: #2d3748;'>{angsuran_ke}</td></tr><tr"
                        " style='border-bottom: 1px solid #edf2f7;'><td"
                        " style='padding: 10px; font-weight: bold; color:"
                        f" #4a5568;'>SISA ANGSURAN</td><td style='padding: 10px;"
                        f" color: #2d3748;'>{sisa_angsuran}</td></tr><tr><td"
                        " style='padding: 10px; font-weight: bold; color:"
                        " #4a5568;'>SISA HUTANG</td><td style='padding: 10px;"
                        " font-weight: bold; color: #e53e3e; font-size:"
                        f" 16px;'>{sisa_hutang}</td></tr></table></div></div>"
                    )

                    st.markdown(kartu_html, unsafe_allow_html=True)

        else:
            st.info(
                "💡 Masukkan 16 digit NIK KTP lalu klik 'Cek Data' untuk melihat"
                " informasi."
            )

    elif pilihan_menu == "Riwayat Akses Admin":
        st.title("🔐 MENU ADMIN: RIWAYAT AKSES")
        password = st.text_input(
            "Masukkan Password Admin:", type="password"
        )

        if password == "Tactical":
            st.success("✅ Password benar!")
            if os.path.exists(FILE_LOG):
                df_log = pd.read_csv(FILE_LOG)
                st.write(
                    f"Total riwayat pengecekan: {len(df_log)} kali akses."
                )
                st.dataframe(df_log, use_container_width=True)
            else:
                st.info("Belum ada riwayat akses yang tercatat.")
        elif password != "":
            st.error("❌ Password salah!")
        else:
            st.warning("Silakan masukkan password admin untuk melihat data.")