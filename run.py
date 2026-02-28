# run.py

from datetime import datetime, timezone

from core.market_state import MarketState
from core.entry_engine import find_entry
from core.trade_judge import evaluate_trade

from data.cache import load_cache, save_cache
from config.settings import SYMBOL

from telegram.bot import send_message, listen_for_commands
from telegram.formatter import format_trade_signal, format_no_trade


def main():
    # 1️⃣ Load cache (memory box)
    cache = load_cache()

    # 2️⃣ Run market analysis
    state = MarketState()
    state.update_session()
    state.update_htf_bias(SYMBOL)
    state.update_market_regime(SYMBOL)

    # 3️⃣ Save analysis results
    cache["session"] = state.session
    cache["htf_bias"] = state.htf_bias
    cache["bias_reason"] = state.bias_reason
    cache["market_regime"] = state.market_regime

    # ✅ VERY IMPORTANT: save last analysis time
    cache["last_analysis_utc"] = datetime.now(timezone.utc).isoformat()

    save_cache(cache)

    # 4️⃣ Trading gates
    if not state.is_tradable():
        listen_for_commands()
        return

    if state.market_regime != "TRENDING":
        send_message(
            format_no_trade(
                SYMBOL,
                f"Market is {state.market_regime.lower()}."
            )
        )
        listen_for_commands()
        return

    # 5️⃣ Entry detection
    signal = find_entry(SYMBOL, state.htf_bias)
    if not signal:
        listen_for_commands()
        return

    # 6️⃣ Trade quality check
    decision = evaluate_trade(signal, state)
    if not decision.allowed:
        send_message(
            format_no_trade(SYMBOL, decision.reason)
        )
        listen_for_commands()
        return

    # 7️⃣ Approved trade → send Telegram signal
    message = format_trade_signal(SYMBOL, signal, decision)
    send_message(message)

    # Save last trade summary (for /lasttrade)
    cache["last_trade"] = message
    save_cache(cache)

    # 8️⃣ Listen for Telegram commands (delayed model)
    listen_for_commands()


if __name__ == "__main__":
    main()