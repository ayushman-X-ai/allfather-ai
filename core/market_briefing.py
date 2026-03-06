# core/market_briefing.py

from core.market_state import MarketState
from core.entry_engine import find_entry
from core.news_filter import is_news_time
from config.settings import SYMBOLS


def market_briefing():

    report = {}

    # session
    state = MarketState()
    state.update_session()

    report["session"] = state.session

    # trend overview
    trends = []

    for symbol in SYMBOLS:

        state.update_htf_bias(symbol)

        trends.append(f"{symbol}: {state.htf_bias}")

    report["trend"] = trends

    # volatility
    state.update_market_regime(SYMBOLS[0])
    report["volatility"] = state.market_regime

    # best setups
    setups = []

    for symbol in SYMBOLS:

        signal = find_entry(symbol, state.htf_bias)

        if signal:
            setups.append(f"{symbol} {signal.direction}")

    report["setups"] = setups if setups else ["No strong setups"]

    # news risk
    report["news"] = "HIGH" if is_news_time() else "LOW"

    # simple sentiment
    bullish = sum(1 for t in trends if "BULLISH" in t)
    bearish = sum(1 for t in trends if "BEARISH" in t)

    if bullish > bearish:
        sentiment = "Risk-on (buyers stronger)"
    elif bearish > bullish:
        sentiment = "Risk-off (sellers stronger)"
    else:
        sentiment = "Mixed"

    report["sentiment"] = sentiment

    return report