# core/journal.py

import json
from datetime import datetime


FILE = "data/trade_journal.json"


def log_trade(symbol, direction, entry, stop, target):

    try:
        with open(FILE, "r") as f:
            trades = json.load(f)
    except:
        trades = []

    trade = {
        "time": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "direction": direction,
        "entry": entry,
        "stop": stop,
        "target": target,
        "result": None
    }

    trades.append(trade)

    with open(FILE, "w") as f:
        json.dump(trades, f, indent=2)