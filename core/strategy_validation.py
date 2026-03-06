import json
import random


JOURNAL = "data/trade_journal.json"


def load_trades():

    try:
        with open(JOURNAL) as f:
            trades = json.load(f)
    except:
        return []

    return [t for t in trades if t.get("result") in ["WIN", "LOSS"]]


# -----------------------------
# DRAW DOWN SIMULATION
# -----------------------------

def drawdown_analysis():

    trades = load_trades()

    equity = 0
    peak = 0
    max_dd = 0
    losing_streak = 0
    worst_streak = 0

    for t in trades:

        r = 1 if t["result"] == "WIN" else -1

        equity += r

        if equity > peak:
            peak = equity

        drawdown = peak - equity

        if drawdown > max_dd:
            max_dd = drawdown

        if r == -1:
            losing_streak += 1
            worst_streak = max(worst_streak, losing_streak)
        else:
            losing_streak = 0

    return {
        "max_drawdown": max_dd,
        "worst_losing_streak": worst_streak
    }


# -----------------------------
# EXPECTANCY ANALYSIS
# -----------------------------

def expectancy_analysis():

    trades = load_trades()

    wins = 0
    losses = 0

    for t in trades:

        if t["result"] == "WIN":
            wins += 1
        else:
            losses += 1

    total = wins + losses

    if total == 0:
        return {"expectancy": 0}

    winrate = wins / total
    lossrate = losses / total

    avg_win = 1.3
    avg_loss = 1

    expectancy = (winrate * avg_win) - (lossrate * avg_loss)

    return {
        "trades": total,
        "winrate": round(winrate * 100, 2),
        "expectancy": round(expectancy, 3)
    }


# -----------------------------
# MARKET REGIME TESTING
# -----------------------------

def regime_test():

    trades = load_trades()

    trending_wins = 0
    trending_total = 0

    ranging_wins = 0
    ranging_total = 0

    for t in trades:

        regime = t.get("regime")

        if regime == "TRENDING":

            trending_total += 1

            if t["result"] == "WIN":
                trending_wins += 1

        if regime == "RANGING":

            ranging_total += 1

            if t["result"] == "WIN":
                ranging_wins += 1

    trending_rate = 0
    ranging_rate = 0

    if trending_total:
        trending_rate = (trending_wins / trending_total) * 100

    if ranging_total:
        ranging_rate = (ranging_wins / ranging_total) * 100

    return {
        "trending_winrate": round(trending_rate, 2),
        "ranging_winrate": round(ranging_rate, 2)
    }


# -----------------------------
# MONTE CARLO SIMULATION
# -----------------------------

def monte_carlo_simulation(iterations=500):

    trades = load_trades()

    results = []

    for t in trades:
        results.append(1 if t["result"] == "WIN" else -1)

    simulations = []

    for _ in range(iterations):

        equity = 0
        sequence = random.sample(results, len(results))

        for r in sequence:
            equity += r

        simulations.append(equity)

    avg = sum(simulations) / len(simulations)

    return {
        "simulations": iterations,
        "average_equity": round(avg, 2)
    }