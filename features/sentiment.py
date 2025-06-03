# features/sentiment.py

import streamlit as st
import numpy as np
from textblob import TextBlob
import yfinance as yf

def get_news_sentiment(ticker):
    st.subheader("📰 Analisis Sentimen Berita")
    
    try:
        stock = yf.Ticker(ticker)
        company_name = stock.info.get('longName', ticker.split('.')[0])
        st.info(f"Berita terbaru untuk {company_name}")

        # Contoh berita simulasi
        example_news = [
            f"{company_name} melaporkan peningkatan pendapatan kuartalan",
            f"Analis merekomendasikan beli saham {company_name}",
            f"{company_name} menghadapi tantangan regulasi baru",
            f"{company_name} mengumumkan dividen yang lebih tinggi"
        ]

        sentiments = []
        for news in example_news:
            blob = TextBlob(news)
            sentiment = blob.sentiment.polarity
            sentiments.append(sentiment)

            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {news}")
            with col2:
                if sentiment > 0.2:
                    st.success("Positif")
                elif sentiment < -0.2:
                    st.error("Negatif")
                else:
                    st.info("Netral")

        avg_sentiment = np.mean(sentiments) if sentiments else 0
        st.metric("Sentimen Rata-rata", 
                 "Positif" if avg_sentiment > 0.1 else "Negatif" if avg_sentiment < -0.1 else "Netral",
                 f"{avg_sentiment:.2f}")

    except Exception as e:
        st.warning(f"Gagal memuat sentimen: {str(e)}")
