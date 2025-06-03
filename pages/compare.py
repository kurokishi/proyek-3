# pages/compare.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data.data_loader import ambil_data_saham

def show(tickers):
    st.subheader("🆚 Perbandingan Saham")

    data = {}
    for ticker in tickers:
        df = ambil_data_saham(ticker)
        if not df.empty:
            data[ticker] = df['Close']

    if len(data) < 2:
        st.warning("Minimal 2 saham dengan data valid diperlukan")
        return

    df_comp = pd.DataFrame(data).dropna()
    df_norm = df_comp / df_comp.iloc[0] * 100

    fig = go.Figure()
    for tkr in df_norm.columns:
        fig.add_trace(go.Scatter(x=df_norm.index, y=df_norm[tkr], name=tkr))
    fig.update_layout(title="Perbandingan Saham (Normalisasi %)", xaxis_title="Tanggal", yaxis_title="Kinerja")
    st.plotly_chart(fig, use_container_width=True)
