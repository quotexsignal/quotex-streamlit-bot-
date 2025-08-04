# strategy.py
import pandas as pd

def analyze_candle(df):
    signal = "No Signal"
    strategy_used = []
    confidence = 0

    if len(df) < 15:
        return signal, "Insufficient data", confidence

    # === EMA Strategy ===
    df['EMA5'] = df['close'].ewm(span=5, adjust=False).mean()
    df['EMA14'] = df['close'].ewm(span=14, adjust=False).mean()

    if df['EMA5'].iloc[-2] < df['EMA14'].iloc[-2] and df['EMA5'].iloc[-1] > df['EMA14'].iloc[-1]:
        ema_signal = "UP"
    elif df['EMA5'].iloc[-2] > df['EMA14'].iloc[-2] and df['EMA5'].iloc[-1] < df['EMA14'].iloc[-1]:
        ema_signal = "DOWN"
    else:
        ema_signal = None

    if ema_signal:
        strategy_used.append(f"EMA({ema_signal})")

    # === RSI Strategy ===
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    rsi_value = rsi.iloc[-1]

    if rsi_value < 30:
        rsi_signal = "UP"
    elif rsi_value > 70:
        rsi_signal = "DOWN"
    else:
        rsi_signal = None

    if rsi_signal:
        strategy_used.append(f"RSI({rsi_signal})")

    # === Engulfing Pattern ===
    prev = df.iloc[-2]
    curr = df.iloc[-1]

    if (
        curr['open'] < curr['close'] and
        prev['open'] > prev['close'] and
        curr['open'] < prev['close'] and
        curr['close'] > prev['open']
    ):
        engulfing_signal = "UP"
    elif (
        curr['open'] > curr['close'] and
        prev['open'] < prev['close'] and
        curr['open'] > prev['close'] and
        curr['close'] < prev['open']
    ):
        engulfing_signal = "DOWN"
    else:
        engulfing_signal = None

    if engulfing_signal:
        strategy_used.append(f"Engulfing({engulfing_signal})")

    # === Final Decision ===
    votes = [ema_signal, rsi_signal, engulfing_signal]
    up_votes = votes.count("UP")
    down_votes = votes.count("DOWN")

    if up_votes > down_votes:
        signal = "UP"
        confidence = int((up_votes / 3) * 100)
    elif down_votes > up_votes:
        signal = "DOWN"
        confidence = int((down_votes / 3) * 100)
    else:
        signal = "No Signal"
        confidence = 50

    return signal, ", ".join(strategy_used) if strategy_used else "None", confidence
