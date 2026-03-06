import json
import random


def run_monte_carlo(simulations=500):

    try:
        with open("data/trade_journal.json") as f:
            trades = json.load(f)
    except:
        return {"error": "No trade history"}

    results = []

    for t in trades:
        if t.get("result") == "WIN":
            results.append(1)
        elif t.get("result") == "LOSS":
            results.append(-1)

    if not results:
        return {"error": "No finished trades"}

    final_equity = []

    for _ in range(simulations):

        equity = 0
        sequence = random.sample(results, len(results))

        for r in sequence:
            equity += r

        final_equity.append(equity)

    avg = sum(final_equity) / len(final_equity)

    return {
        "simulations": simulations,
        "average_result": round(avg, 2)
    }