# core/sessions.py

from datetime import datetime, timezone


def get_current_session():

    now = datetime.now(timezone.utc)
    hour = now.hour

    # London session
    if 7 <= hour < 12:
        return "LONDON"

    # London + New York overlap
    if 12 <= hour < 16:
        return "OVERLAP"

    # New York
    if 16 <= hour < 21:
        return "NEW_YORK"

    return "ASIAN"