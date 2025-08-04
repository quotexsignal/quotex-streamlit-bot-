# app.py
import streamlit as st
import pandas as pd
import datetime
import time
from strategy import analyze_candle
import yfinance as yf

st.set_page_config(page_title="Quotex Signal Bot", layout="centered")

st.title("📊 Quotex Signal Bot – Mobile Friendly")
st.markdown("**Select OTC Pair, Timeframe, and Click 'Get Signal'**")

# Pair selection
pair = st.selectbox("Select OTC Pair", ["EURUSD", "GBPUSD", "AUDUSD", "USDJPY", "NZDUSD", "USDCAD"])

# Timeframe selection
tf = st.selectbox("Timeframe (minutes)", [1, 3, 5])

# Button to get signal
if st.button("📡 Get Signal"):
    with st.spinner("Analyzing candle... please wait..."):
        try:
            interval = f"{tf}m"
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

        except Exception as e:
            st.error(f"Error: {e}")
