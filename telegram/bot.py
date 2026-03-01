# telegram/bot.py

import os
import requests

from data.cache import load_cache, save_cache
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
    Fetch Telegram updates starting from a specific offset.
    """
    url = f"{BASE_URL}/getUpdates"
    params = {"timeout": 30}

    if offset is not None:
        params["offset"] = offset

    return requests.get(url, params=params, timeout=35).json()


def listen_for_commands():
    """
    Listen for Telegram commands.
    Each command is processed ONLY ONCE.
    Non-command messages are ignored silently.
    """
    cache = load_cache()
    offset = cache.get("telegram_offset")

    updates = get_updates(offset)

    if "result" not in updates or not updates["result"]:
        return

    for update in updates["result"]:
        update_id = update.get("update_id")

        # 🔑 Remember the last handled update
        cache["telegram_offset"] = update_id + 1

        message = update.get("message")
        if not message:
            continue

        text = message.get("text", "")
        if not text:
            continue

        # ✅ Ignore anything that is NOT a command
        if not text.startswith("/"):
            continue

        response = handle_command(text.strip())
        send_message(response)

    save_cache(cache)