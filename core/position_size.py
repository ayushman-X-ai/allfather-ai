def calculate_lot_size(entry, stop, account_size=1000, risk_percent=1):

    risk_amount = account_size * (risk_percent / 100)

    stop_distance = abs(entry - stop)

    if stop_distance == 0:
        return 0

    lot_size = risk_amount / (stop_distance * 100000)

    return round(lot_size, 2)