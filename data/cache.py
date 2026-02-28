# data/cache.py

import json
from pathlib import Path

CACHE_FILE = Path("data/market_cache.json")

def load_cache():
    if not CACHE_FILE.exists():
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def save_cache(data):
    CACHE_FILE.parent.mkdir(exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)