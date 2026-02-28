import os
import requests

API_KEY = os.getenv("TWELVE_DATA_API_KEY")

url = "https://api.twelvedata.com/time_series"
params = {
    "symbol": "EUR/USD",      # IMPORTANT
    "interval": "15min",
    "outputsize": 5,
    "apikey": API_KEY
}

response = requests.get(url, params=params)
print("STATUS CODE:", response.status_code)
print("RAW RESPONSE:")
print(response.text)