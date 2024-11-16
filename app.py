import streamlit as st
import pandas as pd
import requests
import json
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Trend Analysis by Zartificial", page_icon="🔍")

# Setup untuk PyTrends
pytrends = TrendReq(hl='en-US', tz=360)

# Desain Sidebar untuk Input
st.sidebar.title("🔍 Analisis Tren Keyword")
st.sidebar.markdown("**Temukan keyword yang sedang tren untuk mendukung strategi SEO Anda.**")

# Input Kata Kunci
keyword = st.sidebar.text_input("Masukkan Keyword Utama:", "digital marketing")

# Pilih jangka waktu dengan penjelasan yang lebih jelas
timeframe = st.sidebar.selectbox(
    "Pilih Periode Waktu",
    [
        "today 1-m: Satu bulan terakhir",
        "today 3-m: Tiga bulan terakhir",
        "today 12-m: Dua belas bulan terakhir (satu tahun)",
        "today 5-y: Lima tahun terakhir",
        "all: Semua data tren yang tersedia"
    ]
)

# Menyimpan pilihan timeframe ke dalam format yang sesuai untuk pytrends
timeframe_mapping = {
    "today 1-m: Satu bulan terakhir": "today 1-m",
    "today 3-m: Tiga bulan terakhir": "today 3-m",
    "today 12-m: Dua belas bulan terakhir (satu tahun)": "today 12-m",
    "today 5-y: Lima tahun terakhir": "today 5-y",
    "all: Semua data tren yang tersedia": "all"
}
selected_timeframe = timeframe_mapping[timeframe]

st.sidebar.write("Pilih periode waktu untuk analisis tren.")

# Tombol untuk memulai analisis
if st.sidebar.button("Lihat Tren"):
    if keyword:
        with st.spinner("🔄 Sedang memuat data tren..."):
            # Menjalankan analisis tren dengan pytrends
            pytrends.build_payload([keyword], cat=0, timeframe=selected_timeframe)
            data = pytrends.interest_over_time()

        # Jika data tidak tersedia
        if data.empty:
            st.error("⚠️ Tidak ada data tren untuk keyword tersebut. Coba kata kunci lain.")
        else:
            # Tampilan hasil analisis
            st.title("📈 Analisis Tren Keyword")
            st.write(f"**Keyword:** `{keyword}`")
            st.write(f"**Periode Waktu:** `{selected_timeframe}`")

            st.divider()  # Garis pemisah

            # Visualisasi tren
            st.markdown("### 📊 Tren Volume Pencarian")
            
            # Set style untuk grafik
            sns.set(style="whitegrid")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(data.index, data[keyword], color='teal', linewidth=3, marker='o', markersize=6)
            ax.fill_between(data.index, data[keyword], color="teal", alpha=0.1)
            
            # Efek bayangan pada garis
            for spine in ax.spines.values():
                spine.set_visible(False)
                
            ax.set_xlabel("Tanggal", fontsize=12, color="gray")
            ax.set_ylabel("Volume Pencarian", fontsize=12, color="gray")
            ax.set_title(f"Tren Volume Pencarian untuk '{keyword}'", fontsize=16, color='teal')
            ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
            
            st.pyplot(fig)

            # Rekomendasi kata kunci terkait menggunakan Google Suggest API
            st.divider()  # Garis pemisah
            st.markdown("### 🔍 Rekomendasi Keyword Terkait")
            try:
                # Fungsi untuk mendapatkan rekomendasi keyword dari Google Suggest API
                def get_google_suggestions(keyword):
                    url = f"http://suggestqueries.google.com/complete/search?client=firefox&q={keyword}"
                    response = requests.get(url)
                    suggestions = json.loads(response.text)[1]
                    return suggestions
                
                # Mengambil rekomendasi keyword
                related_keywords = get_google_suggestions(keyword)
                
                # Menampilkan sebagai teks paragraf dengan separator koma
                if related_keywords:
                    keyword_text = ", ".join(related_keywords)
                    st.markdown("**Hasil Rekomendasi Keyword:**")
                    st.write(keyword_text)
                else:
                    st.warning("⚠️ Tidak ada rekomendasi keyword yang ditemukan.")

            except Exception as e:
                st.error("⚠️ Terjadi kesalahan saat mengambil rekomendasi keyword.")
                st.write(f"Detail kesalahan: {e}")
            
            st.divider()  # Garis pemisah
            # Menampilkan data frame
            st.markdown("### 📅 Data Volume Pencarian")
            st.dataframe(data[[keyword]].style.format(precision=2).highlight_max(color="lightblue"), use_container_width=True)

    else:
        st.error("⚠️ Silakan masukkan keyword terlebih dahulu.")
else:
    # Deskripsi aplikasi
    st.title("📊 Analisis Tren Keyword untuk SEO")
    st.write("""Aplikasi ini memungkinkan Anda untuk mengidentifikasi tren kata kunci terbaru dan memahami volume pencarian dalam periode waktu tertentu.
    Gunakan data ini untuk meningkatkan strategi SEO Anda.""")
    st.markdown("""
    **Cara Menggunakan Aplikasi:**
    1. Masukkan keyword yang ingin dianalisis pada sidebar.
    2. Pilih periode waktu yang relevan.
    3. Tekan tombol "Lihat Tren" untuk melihat hasil analisis.
    """)
    st.sidebar.markdown("**Powered by Streamlit & PyTrends**")
