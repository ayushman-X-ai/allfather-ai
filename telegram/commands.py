# telegram/commands.py

from datetime import datetime, timezone
from data.cache import load_cache


def minutes_since_last_analysis(cache):
    ts = cache.get("last_analysis_utc")
    if not ts:
        return "a while ago"

    last = datetime.fromisoformat(ts)
    now = datetime.now(timezone.utc)
    minutes = int((now - last).total_seconds() / 60)
    return f"{minutes} minute(s) ago"


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

    # We don’t lecture — we gently guide
    return "I didn’t understand that. Try /status or /bias 🙂"


# ---------------- RESPONSES ---------------- #

def format_status_from_cache(cache):
    session = cache.get("session", "UNKNOWN")
    regime = cache.get("market_regime", "UNKNOWN")
    last_seen = minutes_since_last_analysis(cache)

    return (
        "📊 Market check (EURUSD)\n\n"
        f"Right now, the session is: {session}\n"
        f"Market condition looks: {regime.lower()}\n\n"
        f"⏱ Last time I checked: {last_seen}\n\n"
        "If things look messy or slow, waiting is usually the smart move."
    )


def format_bias_from_cache(cache):
    bias = cache.get("htf_bias", "UNKNOWN")
    reason = cache.get("bias_reason", "Nothing clear yet.")
    last_seen = minutes_since_last_analysis(cache)

    return (
        "🧭 Bigger picture view (EURUSD)\n\n"
        f"The higher timeframe bias looks: {bias}\n\n"
        f"Why I think that:\n"
        f"{reason}\n\n"
        f"⏱ Last checked: {last_seen}"
    )


def format_why_from_cache(cache):
    regime = cache.get("market_regime", "UNKNOWN")
    last_seen = minutes_since_last_analysis(cache)

    if regime != "TRENDING":
        return (
            "⛔ Why there’s no trade right now\n\n"
            f"The market is currently {regime.lower()}, "
            f"which usually means price is moving without clarity.\n\n"
            f"⏱ Last checked: {last_seen}\n\n"
            "Staying out here is a form of risk management."
        )

    return (
        "✅ Market conditions are okay overall.\n\n"
        "If you didn’t get a signal, it simply means "
        "the entry wasn’t clean enough yet.\n\n"
        f"⏱ Last checked: {last_seen}"
    )


def format_lasttrade_from_cache(cache):
    last_trade = cache.get("last_trade")

    if not last_trade:
        return (
            "📌 Last trade\n\n"
            "I haven’t sent any trade ideas yet.\n"
            "That usually means the market hasn’t offered a clean opportunity."
        )

    return (
        "📌 Last trade idea I shared\n\n"
        f"{last_trade}"
    )