# core/trade_judge.py

from core.confidence_model import get_confidence_multiplier


class TradeDecision:

    def __init__(self, allowed, rr, confidence, reason):
        self.allowed = allowed
        self.rr = rr
        self.confidence = confidence
        self.reason = reason


def evaluate_trade(signal, market_state):

    entry = signal.entry
    stop = signal.stop_loss

    risk = abs(entry - stop)

    if risk <= 0:
        return TradeDecision(False, 0, 0, "Invalid stop loss level.")

    reward = risk * 1.3
    rr = round(reward / risk, 2)

    base_confidence = 60

    if market_state.market_regime == "TRENDING":
        base_confidence += 10

    if market_state.htf_bias != "NEUTRAL":
        base_confidence += 10

    # AI confidence multiplier
    multiplier = get_confidence_multiplier(
        signal.symbol if hasattr(signal, "symbol") else "UNKNOWN",
        signal.direction
    )

    confidence = int(base_confidence * multiplier)

    if confidence < 55:
        return TradeDecision(
            False,
            rr,
            confidence,
            "Historical performance suggests this setup is weaker."
        )

    return TradeDecision(
        True,
        rr,
        confidence,
        "The setup aligns with both current market structure and past performance."
    )