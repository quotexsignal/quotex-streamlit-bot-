import pandas as pd
import ta

def analyze_candle(df):
    df = df.copy()

    # EMA aur RSI indicators calculate karo
    df['ema20'] = ta.trend.ema_indicator(df['close'], window=20)
    df['rsi'] = ta.momentum.rsi(df['close'], window=14)

    # Last 2 candles le lo
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    signal = None
    reason = []

    # EMA ke upar/below price check karo
    if latest['close'] > latest['ema20']:
        reason.append("Price above EMA20 (Bullish)")
    else:
        reason.append("Price below EMA20 (Bearish)")

    # RSI condition
    if latest['rsi'] > 70:
        reason.append("RSI overbought (>70)")
        signal = "DOWN"
    elif latest['rsi'] < 30:
        reason.append("RSI oversold (<30)")
        signal = "UP"
    else:
        # Simple candle pattern check (bullish/bearish engulfing)
        if latest['close'] > latest['open'] and prev['close'] < prev['open']:
            reason.append("Bullish engulfing pattern")
            signal = "UP"
        elif latest['close'] < latest['open'] and prev['close'] > prev['open']:
            reason.append("Bearish engulfing pattern")
            signal = "DOWN"
        else:
            signal = "No clear signal"
            reason.append("No strong pattern found")

    return signal, reason
    
