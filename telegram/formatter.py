# telegram/formatter.py

from core.position_size import calculate_lot_size


def format_trade_signal(symbol, signal, decision):

    direction = signal.direction
    entry = round(signal.entry, 5)
    stop = round(signal.stop_loss, 5)

    if direction == "BUY":
        target = round(entry + (entry - stop) * 1.3, 5)
    else:
        target = round(entry - (stop - entry) * 1.3, 5)

    lot = calculate_lot_size(signal.entry, signal.stop_loss)

    return (

        f"Possible trade idea on {symbol}\n\n"

        f"What the market looks like:\n"
        f"{signal.reason}\n\n"

        f"Trade plan:\n"
        f"{direction} near: {entry}\n"
        f"Stop loss: {stop}\n"
        f"Possible target area: {target}\n\n"

        f"Confidence in this setup: {decision.confidence}%\n\n"

        f"Suggested position size example:\n"
        f"Around {lot} lots if risking about 1% on a $1000 account.\n\n"

        f"What you can do:\n"
        f"Open MT5 → choose {symbol} → place a {direction} trade near the entry level.\n\n"

        f"Important:\n"
        f"Only enter if price is close to the entry level."
    )


def format_no_trade(symbol, reason):

    return (

        f"No clear opportunity on {symbol} right now.\n\n"

        f"Reason:\n"
        f"{reason}\n\n"

        f"It's usually better to wait for a clearer setup."
    )