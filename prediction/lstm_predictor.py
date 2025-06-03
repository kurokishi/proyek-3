# prediction/lstm_predictor.py

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from data.data_loader import ambil_data_saham
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def run_lstm(ticker, days_ahead=7):
    data = ambil_data_saham(ticker)
    if data.empty:
        st.error("Data tidak tersedia.")
        return

    df = data[["Close"]]
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df)

    # Membuat dataset dengan window (60 hari sebelumnya → 1 prediksi)
    X, y = [], []
    for i in range(60, len(df_scaled)):
        X.append(df_scaled[i-60:i, 0])
        y.append(df_scaled[i, 0])
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    # Buat model LSTM
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(X.shape[1], 1)))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=10, batch_size=32, verbose=0)

    # Prediksi ke depan (berdasarkan harga terakhir)
    last_60 = df_scaled[-60:].reshape(1, 60, 1)
    preds = []
    for _ in range(days_ahead):
        pred = model.predict(last_60)[0][0]
        preds.append(pred)
        last_60 = np.append(last_60[:, 1:, :], [[[pred]]], axis=1)

    pred_actual = scaler.inverse_transform(np.array(preds).reshape(-1, 1)).flatten()
    future_dates = pd.date_range(start=df.index[-1] + pd.Timedelta(days=1), periods=days_ahead)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index[-100:], y=df["Close"].values[-100:], name="Harga Historis"))
    fig.add_trace(go.Scatter(x=future_dates, y=pred_actual, name="Prediksi LSTM", line=dict(color="orange")))
    fig.update_layout(title=f"Prediksi Harga Saham {ticker} (LSTM)", xaxis_title="Tanggal", yaxis_title="Harga")
    st.plotly_chart(fig, use_container_width=True)
