import streamlit as st
import time
from strategy import analyze

st.set_page_config(page_title="Quotex Signal Bot", layout="centered")

st.title("📊 Quotex Signal Bot (OTC)")
st.write("Select your OTC pair and timeframe to get signal at 45 seconds of candle.")

# User inputs
pair = st.selectbox("Select OTC Pair", ["EURUSD-OTC", "GBPUSD-OTC", "USDJPY-OTC", "AUDCAD-OTC", "EURJPY-OTC"])
timeframe = st.selectbox("Select Timeframe", ["1m", "3m", "5m"])

# Signal button
if st.button("🚀 Get Signal"):
    with st.spinner("Analyzing... Waiting for 45s mark of the candle..."):
        current_seconds = int(time.strftime("%S"))
        wait_time = (45 - current_seconds) % 60
        time.sleep(wait_time)

        signal = analyze(pair, timeframe)
        st.success(f"✅ Signal for next candle: **{signal}**")
