
from typer import Typer
import requests
from pathlib import Path
import json

app = Typer()

@app.command("refresh")
def refresh_tokens():
    print("🔄 Fetching token list from CoinGecko...")
    response = requests.get("https://api.coingecko.com/api/v3/coins/list")
    if response.status_code != 200:
        print(f"❌ Failed to fetch: {response.status_code} - {response.text}")
        return

    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    path = data_dir / "coingecko_tokens.json"
    path.write_text(json.dumps(response.json(), indent=2))
    print(f"✅ Token list saved to {path}")
