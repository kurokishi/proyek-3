# pages/dashboard.py

import streamlit as st
import plotly.graph_objects as go
from data.data_loader import ambil_data_saham
from config import format_rupiah
from features import fundamental

def show(ticker):
    st.subheader("📈 Grafik Harga Saham")
    data = ambil_data_saham(ticker)
    
    if not data.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Harga Penutupan'))
        fig.update_layout(title=f"Harga Saham {ticker}", xaxis_title="Tanggal", yaxis_title="Harga (Rp)")
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Harga Terakhir", format_rupiah(data['Close'].iloc[-1]))
        with col2:
            change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
            pct_change = (change / data['Close'].iloc[-2]) * 100
            st.metric("Perubahan Hari Ini", format_rupiah(change), f"{pct_change:.2f}%")
        with col3:
            st.metric("Volume Hari Ini", f"{data['Volume'].iloc[-1]:,}".replace(",", "."))
        
        fundamental.show_fundamental_analysis(ticker)
    else:
        st.warning("Data saham tidak tersedia")

def show_fundamental(ticker):
    fundamental.show_fundamental_analysis(ticker)
