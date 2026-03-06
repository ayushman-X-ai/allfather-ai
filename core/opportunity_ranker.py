from config.settings import SYMBOLS
from core.entry_engine import find_entry
from core.market_state import MarketState
from core.trade_judge import evaluate_trade


def score_setup(signal, state, decision):

    score = 0

    if state.htf_bias != "NEUTRAL":
        score += 20

    if state.market_regime == "TRENDING":
        score += 15

    if decision.confidence > 70:
        score += 20

    if state.session in ["LONDON", "OVERLAP"]:
        score += 15

    rr_score = min(decision.rr * 10, 20)
    score += rr_score

    return int(score)


def find_best_opportunity():

    best = None
    best_score = 0

    for symbol in SYMBOLS:

        state = MarketState()

        state.update_session()
        state.update_htf_bias(symbol)
        state.update_market_regime(symbol)

        signal = find_entry(symbol, state.htf_bias)

        if not signal:
            continue

        decision = evaluate_trade(signal, state)

        if not decision.allowed:
            continue

        score = score_setup(signal, state, decision)

        if score > best_score:

            best_score = score

            best = {
                "symbol": symbol,
                "direction": signal.direction,
                "entry": signal.entry,
                "stop": signal.stop_loss,
                "confidence": decision.confidence,
                "score": score,
                "reason": signal.reason
            }

    return best