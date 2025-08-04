app.py

import streamlit as st
import pandas as pd
import datetime
import time
import yfinance as yf
from strategy import analyze_candle
# Line 7
st.set_page_config(page_title="📊 Quotex Signal Bot", layout="centered")

# Line 8
st.title("📈 Quotex Signal Bot (Accurate | Manual | Auto Refresh)")

--- OTC Pairs ---

otc_pairs = [ "EURUSD", "GBPUSD", "AUDUSD", "USDJPY", "NZDUSD", "USDCAD", "USDCHF", "EURGBP", "EURJPY", "GBPJPY" ]

--- UI Controls ---

pair = st.selectbox("Select OTC Pair", otc_pairs) tf = st.selectbox("Select Timeframe (minutes)", [1, 3, 5])

generate = st.button("📡 Generate Signal") countdown_placeholder = st.empty()

if generate: with st.spinner("Analyzing latest candles..."): try: interval = f"{tf}m" end_time = datetime.datetime.now() start_time = end_time - datetime.timedelta(minutes=30)

data = yf.download(pair + "=X", start=start_time, end=end_time, interval=interval)
        df = data[['Open', 'High', 'Low', 'Close']].copy()
        df.columns = ['open', 'high', 'low', 'close']
        df.dropna(inplace=True)

        signal, strategy, confidence = analyze_candle(df)

        st.success(f"🔮 **Next Candle Prediction: {signal}**")
        st.info(f"📌 Strategy Used: {strategy}")
        st.warning(f"🎯 Confidence Score: {confidence}%")

        # Countdown
        for i in range(60, 0, -1):
            countdown_placeholder.markdown(f"⏳ **Refreshing in:** {i} seconds")
            time.sleep(1)
        st.rerun()

    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

