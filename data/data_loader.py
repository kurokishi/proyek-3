# data/data_loader.py
import os
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def ambil_data_saham(ticker, cache_dir="cache", ttl_jam=1):
    os.makedirs(cache_dir, exist_ok=True)
    path_hist = os.path.join(cache_dir, f"{ticker}_hist.csv")
    now = datetime.now()

    def cache_valid(path):
        return os.path.exists(path) and (now - datetime.fromtimestamp(os.path.getmtime(path))) < timedelta(hours=ttl_jam)

    if cache_valid(path_hist):
        try:
            df = pd.read_csv(path_hist, index_col=0, parse_dates=True)
            df.index = df.index.tz_localize(None)
            return df
        except:
            pass

    try:
        saham = yf.Ticker(ticker)
        hist = saham.history(period="1y", interval="1d")
        if not hist.empty:
            hist.index = hist.index.tz_localize(None)
            hist.to_csv(path_hist)
            return hist
    except:
        pass

    return pd.DataFrame()
