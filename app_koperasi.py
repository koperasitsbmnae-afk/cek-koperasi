if s1 is not None:
    with st.form(key="search_form"):
        nik_input = st.text_input(
            "MASUKKAN NIK KTP",
            placeholder="Ketik 16 digit NIK KTP...",
            key="widget_nik_input"
        )
        
        st.write("")
        
        # Menggunakan 2 kolom sejajar di dalam form agar ukuran tombol kembar identik
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            cek_clicked = st.form_submit_button("🔍 Cek Data", type="primary", use_container_width=True)
        with col_btn2:
            tutup_clicked = st.form_submit_button("🔒 Tutup / Bersihkan", use_container_width=True)

    # Logika aksi tombol
    if tutup_clicked:
        reset_form_callback()
        st.rerun()

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