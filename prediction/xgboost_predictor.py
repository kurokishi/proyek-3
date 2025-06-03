# prediction/xgboost_predictor.py

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import xgboost as xgb
from data.data_loader import ambil_data_saham
from features.technical import add_technical_indicators

def run_xgboost(ticker, days_ahead=7):
    data = ambil_data_saham(ticker)
    if data.empty:
        st.error("Data tidak tersedia.")
        return

    df = add_technical_indicators(data.copy())
    df = df.dropna()
    df['Target'] = df['Close'].shift(-days_ahead)
    df = df.dropna()

    features = ['SMA_20', 'SMA_50', 'RSI', 'MACD', 'Signal']
    X = df[features]
    y = df['Target']

    X_train, y_train = X[:-days_ahead], y[:-days_ahead]
    X_test = X[-days_ahead:]

    model = xgb.XGBRegressor()
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    dates = df.index[-days_ahead:]
    actual = df['Close'].iloc[-100:]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=actual.index, y=actual, name="Harga Historis"))
    fig.add_trace(go.Scatter(x=dates, y=pred, name="Prediksi XGBoost", line=dict(color="green")))
    fig.update_layout(title=f"Prediksi Harga Saham {ticker} (XGBoost)", xaxis_title="Tanggal", yaxis_title="Harga")
    st.plotly_chart(fig, use_container_width=True)
