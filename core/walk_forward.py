# core/walk_forward.py

from core.backtester import run_backtest


def walk_forward():

    segments = 5
    results = []

    for _ in range(segments):

        r = run_backtest()

        results.append(r["winrate"])

    avg = sum(results) / len(results)

    return {
        "segments": segments,
        "average_winrate": round(avg, 2),
        "segment_results": results
    }