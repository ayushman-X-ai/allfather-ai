# core/performance.py

import json


def get_performance():

    try:
        with open("data/trade_journal.json", "r") as f:
            trades = json.load(f)
    except:
        return {
            "total": 0,
            "wins": 0,
            "losses": 0,
            "winrate": 0
        }

    wins = 0
    losses = 0

    for t in trades:
        result = t.get("result")

        if result == "WIN":
            wins += 1
        elif result == "LOSS":
            losses += 1

    total = wins + losses

    winrate = 0
    if total > 0:
        winrate = round((wins / total) * 100, 2)

    return {
        "total": total,
        "wins": wins,
        "losses": losses,
        "winrate": winrate
    }