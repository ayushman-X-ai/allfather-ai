# core/daily_briefing.py

from datetime import datetime, timezone

from core.market_briefing import market_briefing
from core.alert_manager import can_send_alert

from telegram.bot import send_message


def send_daily_briefing():

    now = datetime.now(timezone.utc)

    # Only trigger around London open
    if now.hour != 7:
        return

    # Prevent duplicates (24 hour cooldown)
    if not can_send_alert("daily_briefing", 86400):
        return

    report = market_briefing()

    message = "Daily Trading Briefing\n\n"

    message += f"Session: {report['session']}\n\n"

    message += "Trend Overview\n"

    for t in report["trend"]:
        message += f"{t}\n"

    message += f"\nVolatility: {report['volatility']}\n"

    message += "\nBest Setups\n"

    for s in report["setups"]:
        message += f"{s}\n"

    message += f"\nNews Risk: {report['news']}\n"

    send_message(message)