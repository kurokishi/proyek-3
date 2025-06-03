# config.py

import streamlit as st

def get_tickers():
    tickers_input = st.sidebar.text_input("Masukkan kode saham (pisahkan koma)", value="UNVR.JK, TLKM.JK")
    return [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

def format_rupiah(x):
    try:
        return f"Rp{round(x):,}".replace(",", ".")
    except:
        return "Rp0"

