import pandas as pd
import numpy as np

def analyze_candle(df):
    df['EMA5'] = df['close'].ewm(span=5, adjust=False).mean()
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()

    last_candle = df.iloc[-1]
    if last_candle['EMA5'] > last_candle['EMA20']:
        signal = "UP"
    else:
        signal = "DOWN"

    return signal
        last = df.iloc[-1]
        prev = df.iloc[-2]

        # --- Strategy checks ---
        strategy_used = []
        scores = []

        # EMA Strategy
        if last['EMA5'] > last['EMA20']:
            strategy_used.append("EMA Bullish")
            scores.append(30)
            ema_signal = "UP"
        else:
            strategy_used.append("EMA Bearish")
            scores.append(30)
            ema_signal = "DOWN"

        # RSI Strategy
        if last['RSI'] < 30:
            strategy_used.append("RSI Oversold")
            scores.append(25)
            rsi_signal = "UP"
        elif last['RSI'] > 70:
            strategy_used.append("RSI Overbought")
            scores.append(25)
            rsi_signal = "DOWN"
        else:
            strategy_used.append("RSI Neutral")
            scores.append(10)
            rsi_signal = ema_signal  # fallback

        # Candle Pattern
        if prev['close'] < prev['open'] and last['close'] > last['open'] and last['close'] > prev['open']:
            strategy_used.append("Bullish Engulfing")
            scores.append(40)
            pattern_signal = "UP"
        elif prev['close'] > prev['open'] and last['close'] < last['open'] and last['close'] < prev['open']:
            strategy_used.append("Bearish Engulfing")
            scores.append(40)
            pattern_signal = "DOWN"
        else:
            strategy_used.append("No Pattern")
            scores.append(10)
            pattern_signal = ema_signal  # fallback

        # Final Decision by majority
        decisions = [ema_signal, rsi_signal, pattern_signal]
        final_signal = max(set(decisions), key=decisions.count)
        confidence = min(95, sum(scores))  # cap at 95%

        return final_signal, confidence, ", ".join(strategy_used)

    except Exception as e:
        return "ERROR", 0, f"Error during analysis: {str(e)}"

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=period).mean()
    avg_loss = pd.Series(loss).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
