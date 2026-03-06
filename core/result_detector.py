import json
from data.fetcher import fetch_candles


def update_trade_results():

    try:
        with open("data/trade_journal.json") as f:
            trades = json.load(f)
    except:
        return

    for trade in trades:

        if trade["result"] is not None:
            continue

        candles = fetch_candles(trade["symbol"], timeframe=15, limit=50)

        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]

        if trade["direction"] == "BUY":

            if max(highs) >= trade["target"]:
                trade["result"] = "WIN"

            elif min(lows) <= trade["stop"]:
                trade["result"] = "LOSS"

        else:

            if min(lows) <= trade["target"]:
                trade["result"] = "WIN"

            elif max(highs) >= trade["stop"]:
                trade["result"] = "LOSS"

    with open("data/trade_journal.json", "w") as f:
        json.dump(trades, f, indent=2)