# main.py
import streamlit as st
from pages import dashboard, compare, predictor
from config import get_tickers

def main():
    st.set_page_config(layout="wide", page_title="Analisis Saham Lengkap + AI")

    st.sidebar.title("📊 Menu")
    app_mode = st.sidebar.radio(
        "Pilih Analisis", 
        ["Dashboard Utama", "Analisis Fundamental", "Analisis Teknikal", "Prediksi Harga", "Simulasi Portofolio", "Perbandingan Saham"]
    )

    tickers = get_tickers()
    
    if not tickers:
        st.warning("Silakan masukkan minimal satu kode saham")
        return

    if app_mode == "Perbandingan Saham":
        compare.show(tickers)
    elif len(tickers) > 1:
        st.warning(f"Mode '{app_mode}' hanya tersedia untuk satu saham. Menampilkan perbandingan saham.")
        compare.show(tickers)
    else:
        ticker = tickers[0]
        if app_mode == "Dashboard Utama":
            dashboard.show(ticker)
        elif app_mode == "Analisis Fundamental":
            dashboard.show_fundamental(ticker)
        elif app_mode == "Analisis Teknikal":
            dashboard.show_technical(ticker)
        elif app_mode == "Prediksi Harga":
            predictor.show(ticker)
        elif app_mode == "Simulasi Portofolio":
            dashboard.show_simulation(ticker)

if __name__ == "__main__":
    main()
