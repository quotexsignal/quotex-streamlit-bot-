# strategy.py
import pandas as pd

def analyze_candle(df):
    signal = "No Signal"
    strategy_used = []
    confidence = 0

    if len(df) < 14:
        return signal, "Not enough data", confidence

    # EMA Cross Strategy
    df['EMA5'] = df['close'].ewm(span=5).mean()
    df['EMA14'] = df['close'].ewm(span=14).mean()
    if df['EMA5'].iloc[-2] < df['EMA14'].iloc[-2] and df['EMA5'].iloc[-1] > df['EMA14'].iloc[-1]:
        strategy_used.append("EMA Cross UP")
    elif df['EMA5'].iloc[-2] > df['EMA14'].iloc[-2] and df['EMA5'].iloc[-1] < df['EMA14'].iloc[-1]:
        strategy_used.append("EMA Cross DOWN")

    # RSI
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    rsi_val = rsi.iloc[-1]

    if rsi_val < 30:
        strategy_used.append("RSI Oversold")
    elif rsi_val > 70:
        strategy_used.append("RSI Overbought")

    # Engulfing pattern
    prev = df.iloc[-2]
    curr = df.iloc[-1]
    if curr['open'] < curr['close'] and prev['open'] > prev['close'] and curr['open'] < prev['close'] and curr['close'] > prev['open']:
        strategy_used.append("Bullish Engulfing")
    elif curr['open'] > curr['close'] and prev['open'] < prev['close'] and curr['open'] > prev['close'] and curr['close'] < prev['open']:
        strategy_used.append("Bearish Engulfing")

    # Voting
    up_votes = sum(1 for s in strategy_used if "UP" in s or "Bullish" in s or "Oversold" in s)
    down_votes = sum(1 for s in strategy_used if "DOWN" in s or "Bearish" in s or "Overbought" in s)

    if up_votes > down_votes:
        signal = "UP"
        confidence = int((up_votes / 3) * 100)
    elif down_votes > up_votes:
        signal = "DOWN"
        confidence = int((down_votes / 3) * 100)

    return signal, ", ".join(strategy_used), confidence
