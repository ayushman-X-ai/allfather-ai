# telegram/bot.py

import os
import requests

from telegram.commands import handle_command

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(text):
    """
    Send a message to your Telegram chat.
    """
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, json=payload, timeout=10)


def get_updates(offset=None):
    """
    Fetch Telegram updates.
    """
    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 30}

    if offset is not None:
        params["offset"] = offset

    return requests.get(url, params=params, timeout=35).json()


def listen_for_commands():
    """
    Listen for Telegram commands.
    Only reacts to messages that START with '/'.
    Everything else is ignored silently.
    """
    offset = None
    updates = get_updates(offset)

    if "result" not in updates:
        return

    for update in updates["result"]:
        offset = update["update_id"] + 1

        message = update.get("message")
        if not message:
            continue

        text = message.get("text", "")
        if not text:
            continue

        # ✅ IMPORTANT FIX:
        # Ignore anything that is NOT a command
        if not text.startswith("/"):
            continue

        response = handle_command(text.strip())
        send_message(response)