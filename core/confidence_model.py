# core/confidence_model.py

import json


JOURNAL_FILE = "data/trade_journal.json"


def calculate_winrates():

    try:
        with open(JOURNAL_FILE, "r") as f:
            trades = json.load(f)
    except:
        return {}

    stats = {}

    for trade in trades:

        symbol = trade["symbol"]
        direction = trade["direction"]
        result = trade.get("result")

        key = f"{symbol}_{direction}"

        if key not in stats:
            stats[key] = {"wins": 0, "losses": 0}

        if result == "WIN":
            stats[key]["wins"] += 1

        if result == "LOSS":
            stats[key]["losses"] += 1

    winrates = {}

    for key, value in stats.items():

        total = value["wins"] + value["losses"]

        if total == 0:
            continue

        winrate = value["wins"] / total

        winrates[key] = winrate

    return winrates


def get_confidence_multiplier(symbol, direction):

    winrates = calculate_winrates()

    key = f"{symbol}_{direction}"

    winrate = winrates.get(key, 0.5)

    if winrate > 0.6:
        return 1.1

    if winrate < 0.4:
        return 0.9

    return 1.0