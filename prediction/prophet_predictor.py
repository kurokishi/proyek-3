# prediction/prophet_predictor.py

import streamlit as st
from prophet import Prophet
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from data.data_loader import ambil_data_saham
from config import format_rupiah

def run_prophet(ticker, periode_hari=30):
    hist = ambil_data_saham(ticker)
    if hist.empty:
        st.warning("Tidak ada data historis untuk prediksi.")
        return
    
    split_point = int(len(hist) * 0.8)
    train = hist.iloc[:split_point][['Close']].reset_index()
    test = hist.iloc[split_point:][['Close']].reset_index()

    train.rename(columns={"Date": "ds", "Close": "y"}, inplace=True)
    train['ds'] = pd.to_datetime(train['ds']).dt.tz_localize(None)

    model = Prophet(daily_seasonality=True)
    model.fit(train)

    future = model.make_future_dataframe(periods=len(test))
    forecast = model.predict(future)

    pred_test = forecast.iloc[split_point:]['yhat'].values
    actual_test = test['Close'].values

    mae = np.mean(np.abs(pred_test - actual_test))
    mse = np.mean((pred_test - actual_test)**2)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((actual_test - pred_test) / actual_test)) * 100

    st.subheader("📊 Evaluasi Prediksi Prophet")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("MAE", f"{mae:.2f}")
    col2.metric("MSE", f"{mse:.2f}")
    col3.metric("RMSE", f"{rmse:.2f}")
    col4.metric("MAPE", f"{mape:.2f}%")

    fig_eval = go.Figure()
    fig_eval.add_trace(go.Scatter(x=test['Date'], y=actual_test, name='Harga Aktual', line=dict(color='blue')))
    fig_eval.add_trace(go.Scatter(x=test['Date'], y=pred_test, name='Prediksi Prophet', line=dict(color='red', dash='dash')))
    fig_eval.update_layout(title="Evaluasi Prediksi Prophet", xaxis_title="Tanggal", yaxis_title="Harga")
    st.plotly_chart(fig_eval, use_container_width=True)

    st.subheader("🔮 Prediksi Masa Depan")
    future = model.make_future_dataframe(periods=periode_hari)
    forecast = model.predict(future)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=train['ds'], y=train['y'], name='Training'))
    fig.add_trace(go.Scatter(x=test['Date'], y=test['Close'], name='Testing'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Prediksi'))
    fig.add_trace(go.Scatter(
        x=forecast['ds'].tolist() + forecast['ds'].tolist()[::-1],
        y=forecast['yhat_upper'].tolist() + forecast['yhat_lower'].tolist()[::-1],
        fill='toself', fillcolor='rgba(0,100,80,0.2)', line=dict(color='rgba(255,255,255,0)'), name="Confidence Interval"
    ))
    fig.update_layout(title=f"Prediksi Harga Saham {ticker}", xaxis_title="Tanggal", yaxis_title="Harga")
    st.plotly_chart(fig, use_container_width=True)

    st.write("### Tabel Prediksi")
    prediksi_tampil = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periode_hari)
    prediksi_tampil.columns = ['Tanggal', 'Prediksi', 'Batas Bawah', 'Batas Atas']
    prediksi_tampil['Prediksi'] = prediksi_tampil['Prediksi'].apply(format_rupiah)
    st.dataframe(prediksi_tampil)
