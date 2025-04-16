import requests

COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_token_price(symbol: str):
    try:
        response = requests.get(f"{COINGECKO_API}/simple/price", params={
            "ids": symbol,
            "vs_currencies": "usd"
        })
        response.raise_for_status()
        data = response.json()
        return data.get(symbol, {}).get("usd", None)
    except Exception as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None

def search_token_id(query: str):
    try:
        response = requests.get(f"{COINGECKO_API}/search", params={"query": query})
        response.raise_for_status()
        data = response.json()
        for item in data.get("coins", []):
            if item["symbol"].lower() == query.lower():
                return item["id"]
        return None
    except Exception as e:
        print(f"Error searching for {query}: {e}")
        return None

def get_token_prices_batch(symbol_ids):
    """Takes a list of Coingecko token IDs, returns a dict of prices (USD > 0.01 only)."""
    try:
        if not symbol_ids:
            return {}

        ids = ",".join(symbol_ids)
        response = requests.get(f"{COINGECKO_API}/simple/price", params={
            "ids": ids,
            "vs_currencies": "usd"
        })
        response.raise_for_status()

        data = response.json()
        return {
            k: v.get("usd")
            for k, v in data.items()
            if isinstance(v, dict) and isinstance(v.get("usd"), (int, float)) and v.get("usd", 0) >= 0.01
        }
    except Exception as e:
        print(f"Batch price error: {e}")
        return {}

def get_all_coingecko_symbols():
    try:
        url = f"{COINGECKO_API}/coins/list"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {coin['symbol'].lower() for coin in data}
    except Exception as e:
        print(f"Error fetching token list: {e}")
        return set()

def is_valid_token(symbol: str, valid_symbols: set) -> bool:
    return symbol.lower() in valid_symbols
