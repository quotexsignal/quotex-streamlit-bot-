# strategy.py
import pandas as pd

def analyze_candle(df):
    signal = "No Signal"
    strategy_used = "None"
    confidence = 0

    if len(df) < 14:
        return signal, strategy_used, confidence

    # EMA Strategy
    df['EMA5'] = df['close'].ewm(span=5, adjust=False).mean()
    df['EMA14'] = df['close'].ewm(span=14, adjust=False).mean()
    ema_condition = df['EMA5'].iloc[-2] < df['EMA14'].iloc[-2] and df['EMA5'].iloc[-1] > df['EMA14'].iloc[-1]
    ema_signal = "UP" if ema_condition else "DOWN" if not ema_condition else None

    # RSI Strategy
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    rsi_value = rsi.iloc[-1]
    if rsi_value < 30:
        rsi_signal = "UP"
    elif rsi_value > 70:
        rsi_signal = "DOWN"
    else:
        rsi_signal = None

    # Candle pattern (simple bullish/bearish engulfing)
    prev = df.iloc[-2]
    curr = df.iloc[-1]
    engulfing = None
    if curr['open'] < curr['close'] and prev['open'] > prev['close'] and curr['open'] < prev['close'] and curr['close'] > prev['open']:
        engulfing = "UP"
    elif curr['open'] > curr['close'] and prev['open'] < prev['close'] and curr['open'] > prev['close'] and curr['close'] < prev['open']:
        engulfing = "DOWN"

    # Confidence scoring
    votes = [ema_signal, rsi_signal, engulfing]
    vote_counts = {'UP': votes.count("UP"), 'DOWN': votes.count("DOWN")}
    if vote_counts['UP'] > vote_counts['DOWN']:
        signal = "UP"
        confidence = int((vote_counts['UP'] / 3) * 100)
    elif vote_counts['DOWN'] > vote_counts['UP']:
        signal = "DOWN"
        confidence = int((vote_counts['DOWN'] / 3) * 100)

    strategy_used = ", ".join([s for s in ["EMA", "RSI", "Engulfing"] if s in votes])

    return signal, strategy_used, confidence
