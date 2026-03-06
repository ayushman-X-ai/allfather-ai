# core/entry_engine.py

from data.fetcher import fetch_candles
from core.orderflow import detect_order_block


class EntrySignal:

    def __init__(self, symbol, direction, entry, stop_loss, reason):
        self.symbol = symbol
        self.direction = direction
        self.entry = entry
        self.stop_loss = stop_loss
        self.reason = reason


def detect_liquidity_pools(candles):

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    return max(highs), min(lows)


def find_entry(symbol, htf_bias):

    candles = fetch_candles(symbol, timeframe=15, limit=60)

    if len(candles) < 20:
        return None

    last = candles[-1]

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]
    closes = [c["close"] for c in candles]

    # liquidity pools
    pool_high, pool_low = detect_liquidity_pools(candles[-20:])

    # order block
    order_block = detect_order_block(candles[-5:])

    # ------------------------------
    # BUY SETUPS
    # ------------------------------

    if htf_bias == "BULLISH":

        if closes[-1] > closes[-3]:

            entry = last["close"]

            if order_block and order_block["type"] == "BULLISH":
                stop = order_block["level"]
            else:
                stop = pool_low

            return EntrySignal(
                symbol,
                "BUY",
                entry,
                stop,
                "Price is trending upward and reacting near a bullish order block."
            )

    # ------------------------------
    # SELL SETUPS
    # ------------------------------

    if htf_bias == "BEARISH":

        if closes[-1] < closes[-3]:

            entry = last["close"]

            if order_block and order_block["type"] == "BEARISH":
                stop = order_block["level"]
            else:
                stop = pool_high

            return EntrySignal(
                symbol,
                "SELL",
                entry,
                stop,
                "Price is trending downward and reacting near a bearish order block."
            )

    return None