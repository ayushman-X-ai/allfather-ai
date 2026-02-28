# core/entry_engine.py

from data.fetcher import fetch_candles

class EntrySignal:
    def __init__(self, direction, entry, stop_loss, reason):
        self.direction = direction      # BUY or SELL
        self.entry = entry
        self.stop_loss = stop_loss
        self.reason = reason


def find_entry(symbol, htf_bias):
    """
    Looks for a pullback continuation entry on 5M timeframe.
    Returns EntrySignal or None.
    """

    candles = fetch_candles(symbol, timeframe=5, limit=30)

    if len(candles) < 20:
        return None

    # Use last few candles
    recent = candles[-6:]

    closes = [c["close"] for c in recent]
    highs = [c["high"] for c in recent]
    lows = [c["low"] for c in recent]

    last = recent[-1]
    prev = recent[-2]

    # ---------- BUY LOGIC ----------
    if htf_bias == "BULLISH":
        pullback = closes[-3] < closes[-5]
        rejection = last["close"] > last["open"] and last["low"] < prev["low"]

        if pullback and rejection:
            entry = last["close"]
            stop_loss = min(lows[-5:])

            reason = (
                "Price pulled back slightly in an uptrend and buyers stepped in again."
            )

            return EntrySignal("BUY", entry, stop_loss, reason)

    # ---------- SELL LOGIC ----------
    if htf_bias == "BEARISH":
        pullback = closes[-3] > closes[-5]
        rejection = last["close"] < last["open"] and last["high"] > prev["high"]

        if pullback and rejection:
            entry = last["close"]
            stop_loss = max(highs[-5:])

            reason = (
                "Price pulled back slightly in a downtrend and sellers stepped in again."
            )

            return EntrySignal("SELL", entry, stop_loss, reason)

    return None