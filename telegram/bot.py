# telegram/bot.py

import requests

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from telegram.commands import handle_command


BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

LAST_UPDATE_ID = None


def send_message(text):

    url = f"{BASE_URL}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }

    try:
        requests.post(url, json=payload)
    except:
        pass


def normalize_command(text):

    if not text:
        return ""

    text = text.strip().lower()

    if "@" in text:
        text = text.split("@")[0]

    return text


def listen_for_commands():

    global LAST_UPDATE_ID

    url = f"{BASE_URL}/getUpdates"

    params = {}

    if LAST_UPDATE_ID:
        params["offset"] = LAST_UPDATE_ID + 1

    try:
        response = requests.get(url, params=params).json()
    except:
        return

    if not response.get("result"):
        return

    updates = response["result"]

    for update in updates:

        LAST_UPDATE_ID = update["update_id"]

        message = update.get("message")

        if not message:
            continue

        text = message.get("text")

        if not text:
            continue

        command = normalize_command(text)

        result = handle_command(command)

        if result:
            send_message(result)