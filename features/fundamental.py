# features/fundamental.py

import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf

def show_fundamental_analysis(ticker):
    try:
        stock = yf.Ticker(ticker)
        
        st.subheader("📊 Analisis Fundamental")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Info Perusahaan**")
            info = stock.info
            st.write(f"Nama: {info.get('longName', 'N/A')}")
            st.write(f"Sektor: {info.get('sector', 'N/A')}")
            st.write(f"Industri: {info.get('industry', 'N/A')}")
            st.write(f"Negara: {info.get('country', 'N/A')}")
        
        with col2:
            st.markdown("**Valuasi**")
            st.write(f"P/E: {info.get('trailingPE', 'N/A')}")
            st.write(f"P/B: {info.get('priceToBook', 'N/A')}")
            st.write(f"EPS: {info.get('trailingEps', 'N/A')}")
            st.write(f"Dividen Yield: {info.get('dividendYield', 'N/A')}")
        
        with col3:
            st.markdown("**Kinerja**")
            st.write(f"ROE: {info.get('returnOnEquity', 'N/A')}")
            st.write(f"ROA: {info.get('returnOnAssets', 'N/A')}")
            st.write(f"Profit Margin: {info.get('profitMargins', 'N/A')}")
            st.write(f"Debt/Equity: {info.get('debtToEquity', 'N/A')}")
        
        # Grafik Laporan Keuangan
        st.markdown("**Laporan Keuangan**")
        financials = stock.financials
        if not financials.empty:
            fig, ax = plt.subplots(figsize=(10, 4))
            financials.loc[['Total Revenue', 'Net Income']].T.plot(kind='bar', ax=ax)
            st.pyplot(fig)
    
    except Exception as e:
        st.warning(f"Tidak dapat memuat data fundamental: {str(e)}")
