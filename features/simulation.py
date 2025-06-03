# features/simulation.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from data.data_loader import ambil_data_saham
from config import format_rupiah

def run_multi_simulation(tickers):
    st.subheader("💼 Simulasi Portofolio Multi-Saham")

    default_modal = 10_000_000
    total_modal = st.number_input("Total Modal Investasi (Rp)", min_value=1_000_000, value=default_modal, step=1_000_000)

    default_date = datetime.now() - timedelta(days=180)
    start_date = st.date_input("Tanggal Mulai Investasi", value=default_date)

    st.markdown("### 📊 Alokasi Saham")
    alokasi = {}
    total_alokasi = 0

    for ticker in tickers:
        col1, col2 = st.columns([1, 1])
        with col1:
            persen = st.number_input(f"Alokasi untuk {ticker} (%)", min_value=0, max_value=100, value=int(100/len(tickers)))
        with col2:
            frekuensi = st.selectbox(f"Frekuensi DCA untuk {ticker}", ["Sekali (Lump Sum)", "Bulanan", "Mingguan"], key=f"dca_{ticker}")
        alokasi[ticker] = {"persen": persen, "dca": frekuensi}
        total_alokasi += persen

    if total_alokasi != 100:
        st.error("Total alokasi harus 100%.")
        return

    if st.button("Simulasikan Portofolio"):
        nilai_akhir_total = 0
        df_plot = pd.DataFrame()

        for ticker in tickers:
            data = ambil_data_saham(ticker)
            if data.empty or pd.to_datetime(start_date) not in data.index:
                st.warning(f"Data tidak tersedia untuk {ticker}")
                continue

            alokasi_rp = total_modal * (alokasi[ticker]["persen"] / 100)
            frek = alokasi[ticker]["dca"]
            start_date_clean = pd.to_datetime(start_date).tz_localize(None)

            df = data[data.index >= start_date_clean].copy()
            if df.empty:
                st.warning(f"Tidak ada data setelah {start_date} untuk {ticker}")
                continue

            investasi_points = [df.index[0]]
            if frek == "Bulanan":
                investasi_points = df.resample('30D').first().dropna().index
            elif frek == "Mingguan":
                investasi_points = df.resample('7D').first().dropna().index

            modal_per_dca = alokasi_rp / len(investasi_points)
            total_saham = 0
            for tanggal in investasi_points:
                harga = df.loc[tanggal]['Close']
                jumlah_beli = modal_per_dca / harga
                total_saham += jumlah_beli

            nilai_akhir = total_saham * df['Close'].iloc[-1]
            nilai_akhir_total += nilai_akhir

            df_plot[ticker] = df['Close'] / df['Close'].iloc[0] * modal_per_dca * len(investasi_points)

            st.write(f"📈 **{ticker}**")
            st.write(f"- Jumlah pembelian: {len(investasi_points)} kali")
            st.write(f"- Total saham terkumpul: {total_saham:.2f}")
            st.write(f"- Nilai akhir: {format_rupiah(nilai_akhir)}")

        st.markdown("---")
        st.metric("📊 Nilai Akhir Portofolio", format_rupiah(nilai_akhir_total))

        if not df_plot.empty:
            fig = go.Figure()
            for ticker in df_plot.columns:
                fig.add_trace(go.Scatter(x=df_plot.index, y=df_plot[ticker], name=ticker))
            fig.update_layout(title="Kinerja Portofolio per Saham", xaxis_title="Tanggal", yaxis_title="Rp")
            st.plotly_chart(fig, use_container_width=True)
