# run.py (FINAL – PHASE 1 COMPLETE)

from core.market_state import MarketState
from core.entry_engine import find_entry
from core.trade_judge import evaluate_trade
from data.cache import load_cache, save_cache
from config.settings import SYMBOL
from telegram.bot import send_message
from telegram.formatter import (
    format_trade_signal,
    format_no_trade
)

def main():
    cache = load_cache()

    state = MarketState()
    state.update_session()
    state.update_htf_bias(SYMBOL)
    state.update_market_regime(SYMBOL)

    cache.update({
        "session": state.session,
        "htf_bias": state.htf_bias,
        "bias_reason": state.bias_reason,
        "market_regime": state.market_regime
    })
    save_cache(cache)

    # --- Session Gate ---
    if not state.is_tradable():
        return

    # --- Regime Gate ---
    if state.market_regime != "TRENDING":
        send_message(
            format_no_trade(
                SYMBOL,
                f"Market is {state.market_regime.lower()} and unclear."
            )
        )
        return

    # --- Entry ---
    signal = find_entry(SYMBOL, state.htf_bias)
    if not signal:
        return

    # --- Judge ---
    decision = evaluate_trade(signal, state)
    if not decision.allowed:
        send_message(
            format_no_trade(SYMBOL, decision.reason)
        )
        return

    # --- Approved Trade ---
    send_message(
        format_trade_signal(SYMBOL, signal, decision)
    )

if __name__ == "__main__":
    main()