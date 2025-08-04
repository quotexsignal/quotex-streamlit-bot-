import pandas as pd

def analyze_candle(df):
    df['EMA5'] = df['close'].ewm(span=5, adjust=False).mean()
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['RSI'] = compute_rsi(df['close'], 14)

    last_candle = df.iloc[-1]

    ema_signal = "UP" if last_candle['EMA5'] > last_candle['EMA20'] else "DOWN"
    rsi_signal = "UP" if last_candle['RSI'] < 30 else "DOWN" if last_candle['RSI'] > 70 else "NEUTRAL"

    pattern_signal = "NEUTRAL"
    if (
        df['close'].iloc[-1] > df['open'].iloc[-1] and
        df['close'].iloc[-2] < df['open'].iloc[-2]
    ):
        pattern_signal = "UP"
    elif (
        df['close'].iloc[-1] < df['open'].iloc[-1] and
        df['close'].iloc[-2] > df['open'].iloc[-2]
    ):
        pattern_signal = "DOWN"

    votes = [ema_signal, rsi_signal, pattern_signal]
    up_votes = votes.count("UP")
    down_votes = votes.count("DOWN")

    if up_votes > down_votes:
        return "UP", int((up_votes / 3) * 100)
    elif down_votes > up_votes:
        return "DOWN", int((down_votes / 3) * 100)
    else:
        return "NEUTRAL", 50

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
