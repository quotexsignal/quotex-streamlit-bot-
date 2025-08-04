# app.py
import streamlit as st
import pandas as pd
import datetime
import time
from strategy import analyze_candle
import yfinance as yf

st.set_page_config(page_title="Quotex Signal Bot", layout="centered")

st.title("📊 Quotex Signal Bot – Auto Analysis")
st.markdown("Select OTC Pair and Timeframe. Signal will auto-update.")

# Sidebar options
pair = st.selectbox("Select OTC Pair", ["EURUSD", "GBPUSD", "AUDUSD", "USDJPY", "NZDUSD", "USDCAD"])
tf = st.selectbox("Timeframe (minutes)", [1, 3, 5])

interval = f"{tf}m"
refresh_interval = tf * 60  # seconds

# Countdown Timer
placeholder = st.empty()

# Analysis block
def analyze_and_display():
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(minutes=30)
    data = yf.download(pair + "=X", start=start_time, end=end_time, interval=interval)

    df = data[['Open', 'High', 'Low', 'Close']]
    df.columns = ['open', 'high', 'low', 'close']
    df.dropna(inplace=True)

    signal, strategy, confidence = analyze_candle(df)

    st.success(f"🔮 **Next Candle Prediction: {signal}**")
    st.info(f"📌 Strategy Used: {strategy}")
    st.warning(f"🎯 Confidence Score: {confidence}%")

analyze_and_display()

# Auto-refresh timer
for remaining in range(refresh_interval, 0, -1):
    mins, secs = divmod(remaining, 60)
    placeholder.info(f"⏳ Refreshing in {mins:02}:{secs:02}")
    time.sleep(1)

st.rerun()
