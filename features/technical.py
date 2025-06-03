# features/technical.py

import streamlit as st
import plotly.graph_objects as go
import numpy as np

def add_technical_indicators(data):
    if data.empty:
        return data
    
    # Simple Moving Averages
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp12 = data['Close'].ewm(span=12, adjust=False).mean()
    exp26 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp12 - exp26
    data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    
    return data

def plot_technical_indicators(data, ticker):
    if data.empty:
        st.warning("Data tidak tersedia.")
        return
    
    # Price with Moving Averages
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Harga'))
    fig1.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], name='SMA 20'))
    fig1.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], name='SMA 50'))
    fig1.update_layout(title=f"Moving Averages - {ticker}", xaxis_title="Tanggal", yaxis_title="Harga")
    st.plotly_chart(fig1, use_container_width=True)
    
    # RSI
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data.index, y=data['RSI'], name='RSI'))
    fig2.add_hline(y=30, line_dash="dash", line_color="green")
    fig2.add_hline(y=70, line_dash="dash", line_color="red")
    fig2.update_layout(title=f"RSI (14 hari) - {ticker}", xaxis_title="Tanggal", yaxis_title="RSI")
    st.plotly_chart(fig2, use_container_width=True)
    
    # MACD
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=data.index, y=data['MACD'], name='MACD'))
    fig3.add_trace(go.Scatter(x=data.index, y=data['Signal'], name='Signal'))
    fig3.update_layout(title=f"MACD - {ticker}", xaxis_title="Tanggal", yaxis_title="Nilai")
    st.plotly_chart(fig3, use_container_width=True)

def show_technical_analysis(data, ticker):
    st.subheader("📊 Analisis Teknikal")
    if not data.empty:
        data = add_technical_indicators(data)
        plot_technical_indicators(data, ticker)
    else:
        st.warning("Data saham tidak tersedia")
