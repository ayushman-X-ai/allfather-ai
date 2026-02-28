# telegram/commands.py

from datetime import datetime, timezone
from data.cache import load_cache


# ---------- Helper: time since last analysis ----------
def minutes_since_last_analysis(cache):
    ts = cache.get("last_analysis_utc")
    if not ts:
        return "unknown"

    last = datetime.fromisoformat(ts)
    now = datetime.now(timezone.utc)
    minutes = int((now - last).total_seconds() / 60)
    return f"{minutes} minute(s) ago"


# ---------- Command handler ----------
def handle_command(command):
    cache = load_cache()

    if command == "/status":
        return format_status_from_cache(cache)

    if command == "/bias":
        return format_bias_from_cache(cache)

    if command == "/why":
        return format_why_from_cache(cache)

    if command == "/lasttrade":
        return format_lasttrade_from_cache(cache)

    return "Unknown command. Try /status, /bias, /why, or /lasttrade."


# ---------- Command responses ----------
def format_status_from_cache(cache):
    session = cache.get("session", "UNKNOWN")
    regime = cache.get("market_regime", "UNKNOWN")
    last_seen = minutes_since_last_analysis(cache)

    return (
        "📊 MARKET STATUS – EURUSD\n\n"
        f"Session: {session}\n"
        f"Market Condition: {regime}\n\n"
        f"⏱ Last analysis: {last_seen}\n\n"
        "Note:\nIf the market is not trending, waiting is safer."
    )


def format_bias_from_cache(cache):
    bias = cache.get("htf_bias", "UNKNOWN")
    reason = cache.get("bias_reason", "No explanation available.")
    last_seen = minutes_since_last_analysis(cache)

    return (
        "🧭 MARKET BIAS – EURUSD\n\n"
        f"Bias: {bias}\n\n"
        f"Reason:\n{reason}\n\n"
        f"⏱ Last analysis: {last_seen}"
    )


def format_why_from_cache(cache):
    regime = cache.get("market_regime", "UNKNOWN")
    last_seen = minutes_since_last_analysis(cache)

    if regime != "TRENDING":
        return (
            "⛔ NO TRADE – EURUSD\n\n"
            f"Reason:\nMarket is {regime.lower()}.\n\n"
            f"⏱ Last analysis: {last_seen}\n\n"
            "Waiting protects capital."
        )

    return (
        "✅ Market conditions are okay.\n"
        "If no trade was sent, it means no good entry yet.\n\n"
        f"⏱ Last analysis: {last_seen}"
    )


def format_lasttrade_from_cache(cache):
    last_trade = cache.get("last_trade")

    if not last_trade:
        return "No trade has been sent yet."

    return (
        "📌 LAST TRADE\n\n"
        f"{last_trade}"
    )