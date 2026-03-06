# core/market_state.py

from data.fetcher import fetch_candles
from core.sessions import get_current_session


class MarketState:

    def __init__(self):
        self.session = None
        self.htf_bias = "NEUTRAL"
        self.bias_reason = ""
        self.market_regime = "UNKNOWN"
        self.volatility = "NORMAL"

    def update_session(self):
        self.session = get_current_session()

    def update_htf_bias(self, symbol):

        candles = fetch_candles(symbol, timeframe=60, limit=30)

        if len(candles) < 10:
            return

        closes = [c["close"] for c in candles]

        if closes[-1] > closes[-5]:
            self.htf_bias = "BULLISH"
            self.bias_reason = "Price has been gradually moving upward on the 1H chart."

        elif closes[-1] < closes[-5]:
            self.htf_bias = "BEARISH"
            self.bias_reason = "Price has been gradually moving downward on the 1H chart."

        else:
            self.htf_bias = "NEUTRAL"
            self.bias_reason = "The higher timeframe direction is not very clear."

    def update_market_regime(self, symbol):

        candles = fetch_candles(symbol, timeframe=15, limit=20)

        if len(candles) < 10:
            return

        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]

        movement = max(highs) - min(lows)

        if movement < 0.0007:
            self.market_regime = "RANGING"
        else:
            self.market_regime = "TRENDING"

        # Volatility check
        candle_sizes = [(c["high"] - c["low"]) for c in candles]
        avg_size = sum(candle_sizes) / len(candle_sizes)

        if avg_size < 0.0002:
            self.volatility = "LOW"
        else:
            self.volatility = "NORMAL"

    def is_tradable(self):

        if self.session == "ASIAN":
            return False

        if self.volatility == "LOW":
            return False

        return True