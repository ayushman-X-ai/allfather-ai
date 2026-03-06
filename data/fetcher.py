# data/fetcher.py

import os
import requests

API_KEY = os.getenv("TWELVE_DATA_API_KEY")
BASE_URL = "https://api.twelvedata.com/time_series"

TIMEFRAME_MAP = {
    5: "5min",
    15: "15min",
    60: "1h",
    240: "4h"
}


def fetch_candles(symbol, timeframe, limit=100):
    if timeframe not in TIMEFRAME_MAP:
        return []

    params = {
        "symbol": symbol,
        "interval": TIMEFRAME_MAP[timeframe],
        "outputsize": limit,
        "apikey": API_KEY,
        "format": "JSON"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception:
        return []

    if "values" not in data:
        return []

    candles = []
    for v in data["values"]:
        candles.append({
            "timestamp": v["datetime"],
            "open": float(v["open"]),
            "high": float(v["high"]),
            "low": float(v["low"]),
            "close": float(v["close"])
        })

    # Oldest → newest
    candles.reverse()
    return candles