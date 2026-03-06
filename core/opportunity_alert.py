# core/opportunity_alert.py

from core.opportunity_ranker import find_best_opportunity
from core.alert_manager import can_send_alert

from telegram.bot import send_message


def check_high_confidence_trade():

    trade = find_best_opportunity()

    if not trade:
        return

    # Only alert strong setups
    if trade["score"] < 80:
        return

    # Prevent repeated alerts (30 min cooldown)
    if not can_send_alert("high_confidence_trade", 1800):
        return

    message = (
        "High-Confidence Opportunity\n\n"
        f"Asset: {trade['symbol']}\n"
        f"Direction: {trade['direction']}\n\n"
        f"Confidence Score: {trade['score']}\n\n"
        f"Entry: {round(trade['entry'],5)}\n"
        f"Stop: {round(trade['stop'],5)}"
    )

    send_message(message)