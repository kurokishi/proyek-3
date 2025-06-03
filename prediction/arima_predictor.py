# prediction/arima_predictor.py

import streamlit as st
import numpy as np
import pandas as pd
from datetime import timedelta
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from data.data_loader import ambil_data_saham
from config import format_rupiah

def run_arima(ticker, pred_hari=30):
    st.info(f"Menjalankan ARIMA untuk {ticker}")
    data = ambil_data_saham(ticker)
    if data.empty:
        st.error("Data historis tidak tersedia.")
        return
    
    df = data[["Close"]]
    split_point = int(len(df) * 0.8)
    train = df.iloc[:split_point]
    test = df.iloc[split_point:]

    best_aic = float("inf")
    best_order = None

    for p in range(0, 3):
        for d in range(0, 2):
            for q in range(0, 3):
                try:
                    model = ARIMA(train, order=(p,d,q))
                    result = model.fit()
                    if result.aic < best_aic:
                        best_aic = result.aic
                        best_order = (p,d,q)
                except:
                    continue

    if not best_order:
        st.error("Tidak dapat menemukan parameter ARIMA terbaik.")
        return

    st.success(f"Model terbaik ARIMA{best_order} (AIC={best_aic:.2f})")

    history = [x for x in train['Close']]
    predictions = []

    for t in range(len(test)):
        model = ARIMA(history, order=best_order)
        model_fit = model.fit()
        yhat = model_fit.forecast()[0]
        predictions.append(yhat)
        history.append(test['Close'].iloc[t])

    mae = np.mean(np.abs(predictions - test['Close'].values))
    mse = np.mean((predictions - test['Close'].values)**2)
    rmse = np.sqrt(mse)
    mape = np.mean(np.abs((test['Close'].values - predictions) / test['Close'].values)) * 100

    st.subheader("📊 Evaluasi Prediksi ARIMA")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("MAE", f"{mae:.2f}")
    col2.metric("MSE", f"{mse:.2f}")
    col3.metric("RMSE", f"{rmse:.2f}")
    col4.metric("MAPE", f"{mape:.2f}%")

    fig_eval = go.Figure()
    fig_eval.add_trace(go.Scatter(x=test.index, y=test['Close'], name='Harga Aktual', line=dict(color='blue')))
    fig_eval.add_trace(go.Scatter(x=test.index, y=predictions, name='Prediksi ARIMA', line=dict(color='red', dash='dash')))
    fig_eval.update_layout(title="Evaluasi Prediksi ARIMA", xaxis_title="Tanggal", yaxis_title="Harga")
    st.plotly_chart(fig_eval, use_container_width=True)

    model_final = ARIMA(df, order=best_order).fit()
    forecast = model_final.get_forecast(steps=pred_hari)
    pred_mean = forecast.predicted_mean
    conf_int = forecast.conf_int()
    pred_dates = pd.date_range(start=df.index[-1] + timedelta(days=1), periods=pred_hari)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index[-100:], y=df["Close"].values[-100:], name="Harga Historis"))
    fig.add_trace(go.Scatter(x=pred_dates, y=pred_mean, name="Prediksi"))
    fig.add_trace(go.Scatter(
        x=pred_dates.tolist() + pred_dates.tolist()[::-1],
        y=conf_int.iloc[:, 0].tolist() + conf_int.iloc[:, 1].tolist()[::-1],
        fill='toself', fillcolor='rgba(0,100,80,0.2)', name="Confidence 95%"
    ))
    fig.update_layout(title=f"Prediksi Harga Saham {ticker} (ARIMA)", xaxis_title="Tanggal", yaxis_title="Harga")
    st.plotly_chart(fig, use_container_width=True)

    perubahan = pred_mean.iloc[-1] - df["Close"].iloc[-1]
    perubahan_persen = (perubahan / df["Close"].iloc[-1]) * 100

    col1, col2 = st.columns(2)
    col1.metric("Prediksi Akhir", format_rupiah(pred_mean.iloc[-1]), f"{perubahan_persen:+.2f}%")
    with col2:
        if perubahan > 0.5:
            st.success("🟢 Sinyal: BELI")
        elif perubahan < -0.5:
            st.error("🔴 Sinyal: JUAL")
        else:
            st.info("⚪ Sinyal: TAHAN")
