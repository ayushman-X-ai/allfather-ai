# core/self_learning.py

import json

STATS_FILE = "data/strategy_stats.json"


def get_multiplier():

    try:
        with open(STATS_FILE, "r") as f:
            data = json.load(f)
    except:
        return 1.0

    return data.get("confidence_multiplier", 1.0)


def update_learning(winrate):

    multiplier = 1.0

    if winrate > 60:
        multiplier = 1.1

    elif winrate < 40:
        multiplier = 0.9

    data = {
        "confidence_multiplier": multiplier
    }

    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=2)