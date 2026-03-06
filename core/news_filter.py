import json
from datetime import datetime, timedelta, timezone


def is_news_time():

    try:
        with open("data/news_events.json", "r") as f:
            data = json.load(f)
    except:
        return False

    now = datetime.now(timezone.utc)

    for event in data["events"]:

        event_time = datetime.fromisoformat(event["time_utc"]).replace(tzinfo=timezone.utc)

        if abs((event_time - now).total_seconds()) < 1800:
            return True

    return False