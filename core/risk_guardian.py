# core/risk_guardian.py

import json

from core.alert_manager import can_send_alert
from telegram.bot import send_message


def check_losing_streak():

    try:
        with open("data/trade_journal.json") as f:
            trades = json.load(f)
    except:
        return

    losing_streak = 0

    for t in reversed(trades):

        if t.get("result") == "LOSS":
            losing_streak += 1
        else:
            break

    if losing_streak >= 3:

        # Prevent alert spam (1 hour cooldown)
        if not can_send_alert("risk_alert", 3600):
            return

        send_message(
            "Risk Alert\n\n"
            f"{losing_streak} losses in a row detected.\n\n"
            "Market conditions may currently be unfavorable.\n"
            "Consider reducing risk or pausing trading temporarily."
        )