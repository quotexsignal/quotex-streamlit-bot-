import pandas as pd

def analyze(df):
    # EMA calculate karo
    df['ema'] = df['close'].ewm(span=10, adjust=False).mean()

    # RSI calculate karo
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # Last 2 candles le lo
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    signal = None
    reason = []

    # EMA ke upar/below price check karo
    if latest['close'] > latest['ema']:
        reason.append("Price above EMA")
    else:
        reason.append("Price below EMA")

    # RSI condition
    if latest['rsi'] > 70:
        reason.append("RSI overbought")
        signal = "DOWN"
    elif latest['rsi'] < 30:
        reason.append("RSI oversold")
        signal = "UP"
    else:
        # Simple candle pattern condition
        if latest['close'] > latest['open']:
            reason.append("Bullish candle")
            signal = "UP"
        elif latest['close'] < latest['open']:
            reason.append("Bearish candle")
            signal = "DOWN"
        else:
            signal = "No clear signal"
            reason.append("No strong candle pattern")

    return signal, reason
