import streamlit as st
import pandas as pd
import yfinance as yf
import time
from datetime import datetime
from strategy import analyze_candle

st.set_page_config(page_title="Quotex Signal Bot", layout="centered")

st.title("📈 Quotex Signal Bot (Accurate | Manual | Auto Refresh)")

pair = st.selectbox("Select OTC Pair", ["EURUSD_otc", "USDJPY_otc", "GBPUSD_otc", "AUDCAD_otc"])
tf = st.selectbox("Select Timeframe", ["1m", "3m", "5m", "15m"])
generate = st.button("🔍 Generate Signal")

def fetch_data(pair, tf):
    interval_map = {
        "1m": "1m",
        "3m": "3m",
        "5m": "5m",
        "15m": "15m"
    }
    data = yf.download(tickers=pair.replace("_otc", "") + "=X", period="1d", interval=interval_map[tf])
    data.dropna(inplace=True)
    data = data.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close"})
    return data

if generate:
    with st.spinner("Analyzing..."):
        data = fetch_data(pair, tf)

        if data.empty or len(data) < 20:
            st.error("Not enough data to analyze.")
        else:
            signal, score = analyze_candle(data)
            st.success(f"Next Candle Prediction: **{signal}** 📊 (Confidence: {score}%)")

            # Auto refresh countdown
            for i in range(60, 0, -1):
                st.info(f"⏳ Refreshing in {i} seconds...")
                time.sleep(1)
            st.experimental_rerun()
