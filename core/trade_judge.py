# core/trade_judge.py

class TradeDecision:
    def __init__(self, allowed, rr, confidence, reason):
        self.allowed = allowed          # True / False
        self.rr = rr                    # Risk:Reward
        self.confidence = confidence    # 0–100
        self.reason = reason


def evaluate_trade(signal, market_state):
    """
    Decides if a trade is good enough to send.
    """

    entry = signal.entry
    stop = signal.stop_loss

    # --- Risk calculation ---
    risk = abs(entry - stop)

    if risk <= 0:
        return TradeDecision(
            False, 0, 0,
            "Invalid stop loss placement."
        )

    # --- Reward estimation (conservative) ---
    # For Phase 1 we assume nearest logical continuation
    reward = risk * 1.5
    rr = reward / risk

    if rr < 1.5:
        return TradeDecision(
            False, rr, 40,
            "Reward is not clearly larger than risk."
        )

    # --- Confidence scoring ---
    confidence = 50  # base

    if market_state.htf_bias != "NEUTRAL":
        confidence += 15

    if market_state.market_regime == "TRENDING":
        confidence += 15

    if risk < entry * 0.002:  # not too wide
        confidence += 10

    confidence = min(confidence, 95)

    # --- Final decision ---
    if confidence >= 70:
        return TradeDecision(
            True, rr, confidence,
            "Risk is controlled and reward is reasonable."
        )

    return TradeDecision(
        False, rr, confidence,
        "Overall quality is not strong enough."
    )