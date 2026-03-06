# core/alert_manager.py

import json
import time

STATE_FILE = "data/alert_state.json"


def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def can_send_alert(alert_name, cooldown_seconds):

    state = load_state()

    now = time.time()

    last = state.get(alert_name, 0)

    # If alert was sent recently, block it
    if now - last < cooldown_seconds:
        return False

    # Update timestamp
    state[alert_name] = now
    save_state(state)

    return True