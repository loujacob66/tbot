
import requests
import json
from pathlib import Path

def load_mapping(primary=True):
    path = Path("config/token_mapping.json" if primary else "config/token_mapping_full.json")
    if not path.exists():
        print(f"❌ Missing {path}")
        return {}
    with path.open() as f:
        return json.load(f)

def get_prices(symbols):
    primary_map = load_mapping(primary=True)
    fallback_map = load_mapping(primary=False)

    # Build ID list with fallback lookup
    symbol_to_id = {}
    missing = []

    for symbol in symbols:
        key = symbol.upper()
        if key in primary_map:
            symbol_to_id[key] = primary_map[key]
        elif key in fallback_map:
            symbol_to_id[key] = fallback_map[key]
        else:
            missing.append(key)

    if missing:
        with open("logs/missing_token_mappings.txt", "a") as f:
            for sym in missing:
                f.write(sym + "\n")
        print(f"⚠️ Unmapped symbols: {missing}")

    ids = list(set(symbol_to_id.values()))
    if not ids:
        print("⚠️ No valid CoinGecko IDs to fetch.")
        return {}

    ids_str = ",".join(ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_str}&vs_currencies=usd"

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()

        # Map prices back to symbols
        prices = {}
        for symbol, token_id in symbol_to_id.items():
            if token_id in data and "usd" in data[token_id]:
                prices[symbol] = data[token_id]["usd"]

        return prices
    except Exception as e:
        print(f"⚠️ Failed to fetch prices: {e}")
        return {}
