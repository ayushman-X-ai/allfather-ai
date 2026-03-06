# core/backtester.py

from data.fetcher import fetch_candles
from core.entry_engine import find_entry
from core.trade_judge import evaluate_trade
from core.market_state import MarketState

SYMBOL = "EUR/USD"


def run_backtest():

    candles = fetch_candles(SYMBOL, timeframe=15, limit=500)

    wins = 0
    losses = 0

    for i in range(50, len(candles)-5):

        slice_data = candles[:i]

        state = MarketState()
        state.update_htf_bias(SYMBOL)
        state.update_market_regime(SYMBOL)

        signal = find_entry(SYMBOL, state.htf_bias)

        if not signal:
            continue

        decision = evaluate_trade(signal, state)

        if not decision.allowed:
            continue

        future = candles[i:i+5]

        entry = signal.entry
        stop = signal.stop_loss

        if signal.direction == "BUY":
            target = entry + (entry - stop) * 1.3

            if max(c["high"] for c in future) >= target:
                wins += 1
            elif min(c["low"] for c in future) <= stop:
                losses += 1

        else:
            target = entry - (stop - entry) * 1.3

            if min(c["low"] for c in future) <= target:
                wins += 1
            elif max(c["high"] for c in future) >= stop:
                losses += 1

    total = wins + losses

    if total == 0:
        print("No trades detected")
        return

    winrate = (wins / total) * 100

    print("Backtest Results")
    print("Trades:", total)
    print("Wins:", wins)
    print("Losses:", losses)
    print("Winrate:", round(winrate, 2), "%")


if __name__ == "__main__":
    run_backtest()