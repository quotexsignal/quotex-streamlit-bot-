import streamlit as st
import time
import pandas as pd
from strategy import analyze

st.set_page_config(page_title="Quotex Signal Bot", layout="centered")

st.title("📊 Quotex Signal Bot")
st.write("Select your OTC pair and timeframe. At 45s of each minute, you'll get a signal based on technical analysis.")

# Pair & Timeframe selection
pair = st.selectbox("📌 Select OTC Pair", ["EURUSD-OTC", "GBPUSD-OTC", "AUDCAD-OTC", "USDJPY-OTC"])
timeframe = st.selectbox("⏱️ Timeframe", ["1m", "3m", "5m"])

start = st.button("🚀 Start Signal Bot")

# Simulate candle data
def get_simulated_candles():
    now = pd.Timestamp.now()
    times = [now - pd.Timedelta(minutes=i) for i in range(15)][::-1]

    # Fake OHLCV candle data
    data = {
        "timestamp": times,
        "open": [1.100 + i*0.001 for i in range(15)],
        "high": [1.101 + i*0.001 for i in range(15)],
        "low": [1.099 + i*0.001 for i in range(15)],
        "close": [1.1005 + i*0.001 for i in range(15)],
    }
    df = pd.DataFrame(data)
    return df

# Start Bot
if start:
    st.success(f"✅ Started signal bot for {pair} | TF: {timeframe}")
    while True:
        with st.spinner("⏳ Waiting 45 seconds..."):
            time.sleep(45)

        df = get_simulated_candles()
        signal, reason = analyze(df)

        st.write(f"📢 **Signal for {pair} ({timeframe})**: `{signal}`")
        st.write("🧠 Reason:", ", ".join(reason))
