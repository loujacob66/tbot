
import json
from pathlib import Path

def load_token_index():
    path = Path(__file__).parent.parent / "data" / "coingecko_tokens.json"
    if not path.exists():
        print("⚠️ CoinGecko token index not found. Skipping validation.")
        return {}
    raw = json.loads(path.read_text())
    return {entry["symbol"].upper(): entry["id"] for entry in raw if entry.get("symbol") and entry.get("id")}

def validate_mentions(mentions, token_index):
    return [m for m in mentions if m in token_index]
