import streamlit as st
import time
from datetime import datetime
import yfinance as yf
from strategy import analyze_candle

# OTC Pairs list (temporary yfinance symbols)
pairs = {
    "EUR/USD OTC": "EURUSD=X",
    "GBP/USD OTC": "GBPUSD=X",
    "USD/JPY OTC": "JPY=X"
}

st.title("📊 Quotex OTC Signal Bot")

# Dropdowns
selected_pair = st.selectbox("Select OTC Pair:", list(pairs.keys()))
selected_timeframe = st.selectbox("Select Timeframe (min):", [1, 5, 15])

# Signal Button
if st.button("🔍 Generate Signal"):
    st.info("⏳ Waiting for 45th second...")

    # Wait till 45th second
    now = datetime.utcnow()
    wait_seconds = 45 - now.second
    if wait_seconds > 0:
        time.sleep(wait_seconds)

    # Convert selected TF to yfinance format
    tf_map = {1: "1m", 5: "5m", 15: "15m"}
    tf_str = tf_map[selected_timeframe]

    try:
        # Download candle data
        data = yf.download(tickers=pairs[selected_pair], period="2d", interval=tf_str)
        data = data.rename(columns={"Open": "open", "High": "high", "Low": "low", "Close": "close"})

        # Signal Analysis
        signal, reason = analyze_candle(data)

        # Show result
        st.success(f"📈 Signal: {signal}")
        st.markdown("### Strategy Explanation:")
        for r in reason:
            st.markdown(f"- {r}")
    except Exception as e:
        st.error(f"❌ Error: {e}")
