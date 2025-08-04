import pandas as pd

def analyze_candle(df):
    df['EMA5'] = df['Close'].ewm(span=5, adjust=False).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['RSI'] = compute_rsi(df['Close'])

    last_candle = df.iloc[-1]
    ema_signal = "UP" if last_candle['EMA5'] > last_candle['EMA20'] else "DOWN"
    rsi_signal = "UP" if last_candle['RSI'] < 30 else "DOWN" if last_candle['RSI'] > 70 else "NEUTRAL"

    if ema_signal == rsi_signal and rsi_signal != "NEUTRAL":
        signal = ema_signal
        confidence = 90
    elif ema_signal == "UP" and rsi_signal == "NEUTRAL":
        signal = "UP"
        confidence = 70
    elif ema_signal == "DOWN" and rsi_signal == "NEUTRAL":
        signal = "DOWN"
        confidence = 70
    else:
        signal = "NO SIGNAL"
        confidence = 50

    return signal, confidence

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))
