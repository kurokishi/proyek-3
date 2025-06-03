# pages/predictor.py

import streamlit as st
from prediction import prophet_predictor, arima_predictor, xgboost_predictor

def show(ticker):
    st.subheader("🔮 Prediksi Harga Saham")
    tab1, tab2, tab3 = st.tabs(["Prophet", "ARIMA", "XGBoost"])

    with tab1:
        periode = st.slider("Periode Prediksi (hari):", min_value=7, max_value=90, value=30)
        if st.button("Prediksi Prophet"):
            prophet_predictor.run_prophet(ticker, periode)

    with tab2:
        periode_arima = st.slider("Periode ARIMA:", 1, 30, 7)
        if st.button("Prediksi ARIMA"):
            arima_predictor.run_arima(ticker, pred_hari=periode_arima)

    with tab3:
        periode_xgb = st.slider("Hari Prediksi XGBoost:", 1, 30, 7)
        if st.button("Prediksi XGBoost"):
            xgboost_predictor.run_xgboost(ticker, days_ahead=periode_xgb)
