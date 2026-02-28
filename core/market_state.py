# core/market_state.py

from core.sessions import get_active_session
from data.fetcher import fetch_candles

class MarketState:
    def __init__(self):
        self.htf_bias = "NEUTRAL"
        self.market_regime = "NO_TRADE"
        self.session = "NO_TRADE"
        self.volatility = "NORMAL"
        self.bias_reason = ""
        self.last_signal_time = None

    def update_session(self):
        self.session = get_active_session()

    def is_tradable(self):
        return self.session in ["LONDON", "LONDON_NY_OVERLAP"]

    # ---------- NEW PART ----------
    def update_htf_bias(self, symbol):
        candles_1h = fetch_candles(symbol, timeframe=60, limit=50)
        candles_4h = fetch_candles(symbol, timeframe=240, limit=50)

        bias_1h = self._analyze_structure(candles_1h)
        bias_4h = self._analyze_structure(candles_4h)

        # Agreement logic
        if bias_1h == bias_4h and bias_1h != "NEUTRAL":
            self.htf_bias = bias_1h
            self.bias_reason = f"Both 1H and 4H show a clear {bias_1h.lower()} structure."
        else:
            self.htf_bias = "NEUTRAL"
            self.bias_reason = "Higher timeframes do not agree on direction."

    def _analyze_structure(self, candles):
        if len(candles) < 10:
            return "NEUTRAL"

        highs = [c["high"] for c in candles[-10:]]
        lows = [c["low"] for c in candles[-10:]]
        closes = [c["close"] for c in candles[-10:]]

        higher_highs = highs[-1] > highs[-3] > highs[-5]
        higher_lows = lows[-1] > lows[-3] > lows[-5]

        lower_lows = lows[-1] < lows[-3] < lows[-5]
        lower_highs = highs[-1] < highs[-3] < highs[-5]

        if higher_highs and higher_lows:
            return "BULLISH"
        elif lower_lows and lower_highs:
            return "BEARISH"
        else:
            return "NEUTRAL"
        
# core/market_state.py (ADD BELOW)

    def update_market_regime(self, symbol):
        """
        Determine if market is TRENDING, RANGING, or NO_TRADE
        using recent 15M candles.
        """
        candles = fetch_candles(symbol, timeframe=15, limit=40)

        if len(candles) < 20:
            self.market_regime = "NO_TRADE"
            return

        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]
        closes = [c["close"] for c in candles]

        # Measure directional movement
        recent_move = abs(closes[-1] - closes[-20])
        total_range = max(highs[-20:]) - min(lows[-20:])

        # Overlap check
        overlap_count = 0
        for i in range(-10, -1):
            if lows[i] <= highs[i - 1] and highs[i] >= lows[i - 1]:
                overlap_count += 1

        overlap_ratio = overlap_count / 9

        # Decision logic
        if recent_move > (total_range * 0.4) and overlap_ratio < 0.6:
            self.market_regime = "TRENDING"
        elif overlap_ratio >= 0.6:
            self.market_regime = "RANGING"
        else:
            self.market_regime = "NO_TRADE"