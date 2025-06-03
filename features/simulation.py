# features/simulation.py

import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
from data.data_loader import ambil_data_saham
from config import format_rupiah
import pandas as pd

def run_simulation(ticker):
    st.subheader("💰 Simulasi Portofolio")
    data = ambil_data_saham(ticker)
    if data.empty:
        st.warning("Data tidak tersedia")
        return

    col1, col2 = st.columns(2)
    with col1:
        initial_investment = st.number_input("Jumlah Investasi Awal (Rp)", min_value=100000, value=10000000, step=100000)
    with col2:
        investment_date = st.date_input("Tanggal Investasi", 
                                      value=datetime.now() - timedelta(days=180),
                                      min_value=data.index[0].date(),
                                      max_value=data.index[-1].date())

    if st.button("Hitung Kinerja"):
        investment_date = pd.to_datetime(investment_date).tz_localize(None)

        if investment_date < data.index[0] or investment_date > data.index[-1]:
            st.error("Tanggal investasi tidak valid")
            return

        mask = data.index >= investment_date
        if not any(mask):
            st.error("Tidak ada data pada tanggal tersebut")
            return

        start_price = data.loc[mask].iloc[0]['Close']
        current_price = data['Close'].iloc[-1]

        shares = initial_investment / start_price
        current_value = shares * current_price
        profit = current_value - initial_investment
        profit_pct = (profit / initial_investment) * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("Nilai Awal", format_rupiah(initial_investment))
        col2.metric("Nilai Sekarang", format_rupiah(current_value), f"{profit_pct:.2f}%")
        col3.metric("Keuntungan/Rugi", format_rupiah(profit))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'] / start_price * initial_investment,
            name='Nilai Portofolio'
        ))
        fig.add_vline(x=investment_date, line_dash="dash", line_color="green")
        fig.update_layout(
            title="Kinerja Portofolio",
            xaxis_title="Tanggal",
            yaxis_title="Nilai (Rp)"
        )
        st.plotly_chart(fig, use_container_width=True)
