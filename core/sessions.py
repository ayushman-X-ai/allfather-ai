# core/sessions.py

from datetime import datetime, timezone

def get_active_session():
    hour = datetime.now(timezone.utc).hour

    if 7 <= hour < 12:
        return "LONDON"
    elif 12 <= hour < 16:
        return "LONDON_NY_OVERLAP"
    elif 16 <= hour < 21:
        return "NEW_YORK"
    else:
        return "NO_TRADE"