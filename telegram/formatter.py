# telegram/formatter.py

def format_trade_signal(symbol, signal, decision):
    return (
        f"🟢 Trade idea spotted on {symbol}\n\n"
        f"Here’s what’s happening:\n"
        f"Price pulled back in the direction of the main trend, "
        f"and the market is starting to move again.\n\n"
        f"📌 Direction: {signal.direction}\n"
        f"📌 Entry area: {round(signal.entry, 5)}\n"
        f"🛑 Safety stop: {round(signal.stop_loss, 5)}\n\n"
        f"📐 Risk vs Reward: around 1 : {decision.rr}\n"
        f"🤖 Confidence level: {decision.confidence}%\n\n"
        f"Why this makes sense:\n"
        f"{signal.reason}\n\n"
        f"🧘 Take it slow.\n"
        f"If the entry doesn’t feel right when you open MT5, "
        f"it’s completely okay to skip."
    )


def format_no_trade(symbol, reason):
    return (
        f"⛔ No trade right now on {symbol}\n\n"
        f"I’m staying out because:\n"
        f"{reason}\n\n"
        f"This is one of those moments where patience protects your capital."
    )