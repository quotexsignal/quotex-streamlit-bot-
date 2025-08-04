import streamlit as st
import time
from datetime import datetime
import yfinance as yf
from strategy import analyze_candle

# --- Page Settings ---
st.set_page_config(page_title="📊 Quotex Signal Bot", layout="centered")
st.title("📈 Quotex Signal Bot (Accurate | Manual | Auto Refresh)")

# --- OTC Pairs ---
pairs = [
    "EURUSD_otc", "GBPUSD_otc", "USDJPY_otc", "AUDUSD_otc", "NZDUSD_otc",
    "EURGBP_otc", "EURJPY_otc", "GBPJPY_otc", "USDCHF_otc", "USDCAD_otc"
]

selected_pair = st.selectbox("Select OTC Pair", pairs)
timeframe = st.selectbox("Select Timeframe", ["1m", "3m", "5m"])
generate = st.button("🧠 Generate Signal")

if "last_click" not in st.session_state:
    st.session_state.last_click = 0

if generate:
    st.session_state.last_click = time.time()

if st.session_state.last_click > 0:
    now = datetime.now()
    seconds = now.second
    wait_time = 45 - seconds if seconds < 45 else 105 - seconds

    with st.spinner(f"Analyzing candle... waiting for {wait_time} seconds..."):
        time.sleep(wait_time)

    # --- Fetch Candle Data ---
    symbol = selected_pair.replace("_otc", "") + "=X"
    interval_map = {"1m": "1m", "3m": "3m", "5m": "5m"}
    interval = interval_map[timeframe]
    data = yf.download(tickers=symbol, period="2d", interval=interval)

    if data is not None and len(data) >= 10:
        signal, score = analyze_candle(data)
        st.success(f"🔔 Signal: **{signal.upper()}**")
        st.info(f"📊 Confidence Score: {score}%")
    else:
        st.error("❌ Failed to fetch enough data.")

    st.markdown("Refreshing in 60 seconds...")
    time.sleep(60)
    st.rerun()
