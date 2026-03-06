# run.py

import time
from datetime import datetime, timezone

from config.settings import SYMBOLS

from core.market_state import MarketState
from core.entry_engine import find_entry
from core.trade_judge import evaluate_trade

from core.news_filter import is_news_time
from core.journal import log_trade

from core.performance import get_performance
from core.self_learning import update_learning

from core.daily_briefing import send_daily_briefing
from core.risk_guardian import check_losing_streak
from core.opportunity_alert import check_high_confidence_trade

from data.cache import load_cache, save_cache

from telegram.bot import send_message, listen_for_commands
from telegram.formatter import format_trade_signal


# ------------------------------------------------
# SINGLE BOT CYCLE
# ------------------------------------------------

def run_cycle():

    cache = load_cache()

    cache["last_analysis_utc"] = datetime.now(timezone.utc).isoformat()

    save_cache(cache)

    # -----------------------
    # AUTOMATED ALERTS
    # -----------------------

    send_daily_briefing()

    check_losing_streak()

    check_high_confidence_trade()

    # -----------------------
    # NEWS FILTER
    # -----------------------

    if is_news_time():

        send_message(
            "⚠️ Major economic news detected.\n\n"
            "Market conditions may become highly volatile.\n"
            "Waiting until the event passes."
        )

        return

    # -----------------------
    # MARKET SCANNING
    # -----------------------

    for symbol in SYMBOLS:

        state = MarketState()

        state.update_session()
        state.update_htf_bias(symbol)
        state.update_market_regime(symbol)

        if not state.is_tradable():
            continue

        signal = find_entry(symbol, state.htf_bias)

        if not signal:
            continue

        decision = evaluate_trade(signal, state)

        if not decision.allowed:
            continue

        message = format_trade_signal(symbol, signal, decision)

        send_message(message)

        # target estimate
        if signal.direction == "BUY":
            target = signal.entry + (signal.entry - signal.stop_loss) * 1.3
        else:
            target = signal.entry - (signal.stop_loss - signal.entry) * 1.3

        log_trade(
            symbol,
            signal.direction,
            signal.entry,
            signal.stop_loss,
            target
        )

    # -----------------------
    # SELF LEARNING UPDATE
    # -----------------------

    performance = get_performance()

    update_learning(performance["winrate"])


# ------------------------------------------------
# MAIN LOOP (24/7 RUNNER)
# ------------------------------------------------

def main():

    print("ALLFATHER AI Trading Agent started")

    while True:

        try:

            run_cycle()

            # Listen for Telegram commands
            listen_for_commands()

        except Exception as e:

            print("Error occurred:", e)

            send_message(
                "⚠️ ALLFATHER encountered an error but recovered.\n\n"
                f"Error: {str(e)}"
            )

        # Wait before next scan
        time.sleep(300)   # 5 minutes


if __name__ == "__main__":
    main()