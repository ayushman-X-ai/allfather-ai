# core/orderflow.py


def detect_order_block(candles):

    if len(candles) < 5:
        return None

    last = candles[-1]
    prev = candles[-2]

    # bullish order block
    if prev["close"] < prev["open"] and last["close"] > last["open"]:
        return {
            "type": "BULLISH",
            "level": prev["low"]
        }

    # bearish order block
    if prev["close"] > prev["open"] and last["close"] < last["open"]:
        return {
            "type": "BEARISH",
            "level": prev["high"]
        }

    return None