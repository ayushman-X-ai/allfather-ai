# config/settings.py

import os


# ------------------------------------------------
# TELEGRAM SETTINGS
# ------------------------------------------------

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# ------------------------------------------------
# MARKET DATA API
# ------------------------------------------------

TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")


# ------------------------------------------------
# TRADING CONFIG
# ------------------------------------------------

SYMBOLS = [
    "EUR/USD",
    "XAU/USD",
    "NASDAQ",
    "DOW"
]


# Timeframes

HTF_TIMEFRAMES = ["1h", "4h"]
LTF_TIMEFRAMES = ["5min", "15min"]


# ------------------------------------------------
# STRATEGY SETTINGS
# ------------------------------------------------

RISK_PER_TRADE = 0.01

MIN_CONFIDENCE = 70


# Opportunity alert threshold
HIGH_CONFIDENCE_THRESHOLD = 80