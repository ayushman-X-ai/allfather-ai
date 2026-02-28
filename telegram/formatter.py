# telegram/formatter.py

def format_trade_signal(symbol, signal, decision):
    return (
        f"🟢 TRADE SETUP – {symbol}\n\n"
        f"📍 Direction: {signal.direction}\n"
        f"📍 Entry: {round(signal.entry, 5)}\n"
        f"🛑 Stop Loss: {round(signal.stop_loss, 5)}\n\n"
        f"📐 Risk:Reward: 1:{decision.rr}\n"
        f"🤖 Confidence: {decision.confidence}%\n\n"
        f"📝 Explanation:\n"
        f"{signal.reason}\n\n"
        f"⚠️ Reminder:\n"
        f"Capital protection comes first. Don’t rush the entry."
    )


def format_no_trade(symbol, reason):
    return (
        f"⛔ NO TRADE – {symbol}\n\n"
        f"Reason:\n{reason}\n\n"
        f"🧘 Waiting is safer than forcing trades."
    )


def format_status(state):
    return (
        f"📊 MARKET STATUS – EURUSD\n\n"
        f"Session: {state.session}\n"
        f"HTF Bias: {state.htf_bias}\n"
        f"Market Condition: {state.market_regime}\n\n"
        f"Note:\nTrade only when market is clean."
    )


def format_bias(state):
    return (
        f"🧭 MARKET BIAS – EURUSD\n\n"
        f"Bias: {state.htf_bias}\n\n"
        f"Reason:\n{state.bias_reason}"
    )