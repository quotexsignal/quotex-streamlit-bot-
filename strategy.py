import pandas as pd

def analyze_candle(df):
    if df is None or df.empty or 'Close' not in df.columns:
        return "NO DATA", 0

    df['EMA5'] = df['Close'].ewm(span=5, adjust=False).mean()
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()

    df['RSI'] = compute_rsi(df['Close'])

    # Drop NaN values to avoid errors
    df.dropna(inplace=True)

    if df.empty:
        return "NO DATA", 0

    last_candle = df.iloc[-1]

    # EMA Strategy
    ema_signal = "UP" if last_candle['EMA5'] > last_candle['EMA20'] else "DOWN"

    # RSI Strategy
    if last_candle['RSI'] < 30:
        rsi_signal = "UP"
    elif last_candle['RSI'] > 70:
        rsi_signal = "DOWN"
    else:
        rsi_signal = ema_signal

    # Final Decision
    if ema_signal == rsi_signal:
        confidence = 90
        final_signal = ema_signal
    else:
        confidence = 65
        final_signal = ema_signal

    return final_signal, confidence

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
