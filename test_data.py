from data.fetcher import fetch_candles

candles = fetch_candles("EURUSD", timeframe=15, limit=5)

print("Fetched candles:")
for c in candles:
    print(c)