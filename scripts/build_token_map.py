
import requests
import json
from pathlib import Path

def fetch_top_tokens(limit=1000):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={limit}&page=1"
    try:
        res = requests.get(url, timeout=15)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"❌ Failed to fetch top tokens from CoinGecko: {e}")
        return []

def fetch_all_tokens():
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        res = requests.get(url, timeout=30)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        print(f"❌ Failed to fetch all tokens from CoinGecko: {e}")
        return []

def build_mappings():
    print("🔍 Fetching top tokens...")
    top_tokens = fetch_top_tokens()
    top_map = {}

    for token in top_tokens:
        symbol = token["symbol"].upper()
        if symbol not in top_map:
            top_map[symbol] = token["id"]

    print(f"✅ Created top mapping with {len(top_map)} symbols.")

    print("🔍 Fetching full token list...")
    all_tokens = fetch_all_tokens()
    full_map = {}

    for token in all_tokens:
        symbol = token["symbol"].upper()
        if symbol not in full_map:
            full_map[symbol] = token["id"]

    print(f"✅ Created full mapping with {len(full_map)} symbols.")

    return top_map, full_map

def save_mappings(top_map, full_map):
    config_dir = Path("config")
    config_dir.mkdir(exist_ok=True)

    with (config_dir / "token_mapping.json").open("w") as f:
        json.dump(top_map, f, indent=2)
    print("💾 Saved top token mapping to config/token_mapping.json")

    with (config_dir / "token_mapping_full.json").open("w") as f:
        json.dump(full_map, f, indent=2)
    print("💾 Saved full token mapping to config/token_mapping_full.json")

if __name__ == "__main__":
    top, full = build_mappings()
    save_mappings(top, full)
