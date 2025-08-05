import streamlit as st
import time
import yfinance as yf
from strategy import analyze_candle

# Page setup
st.set_page_config(page_title="📈 Quotex Signal Bot", layout="centered")
st.title("📈 Quotex Signal Bot (Accurate | Manual | Auto Refresh)")

# OTC pair selection
pair = st.selectbox("Select OTC Pair", [
    "EURUSD_otc", "GBPUSD_otc", "AUDUSD_otc", "USDJPY_otc", "USDCHF_otc", "NZDUSD_otc"
])

# Timeframe selection
tf = st.selectbox("Select Timeframe", ["1m", "3m", "5m"])

# Function to fetch data from Yahoo Finance
def fetch_data(pair, tf):
    interval_map = {"1m": "1m", "3m": "3m", "5m": "5m"}
    interval = interval_map.get(tf, "1m")
    ticker = pair.replace("_otc", "") + "=X"
    data = yf.download(ticker, period="1d", interval=interval)
    data.rename(columns={
        "Close": "close",
        "Open": "open",
        "High": "high",
        "Low": "low"
    }, inplace=True)
    return data

# Generate Signal button
if st.button("🔍 Generate Signal"):
    with st.spinner("Analyzing... please wait..."):
        try:
            df = fetch_data(pair, tf)
            signal, confidence, strategy = analyze_candle(df)

            st.success(f"📊 Signal: **{signal.upper()}**")
            st.info(f"✅ Confidence: **{confidence}%**")
            st.code(f"📌 Strategy Used: {strategy}")

            # 60-second countdown
            for i in range(60, 0, -1):
                st.write(f"⏱️ Auto-refresh in {i} seconds...")
                time.sleep(1)
            st.experimental_rerun()

        except Exception as e:
            st.error(f"❌ Error during analysis: {str(e)}")
