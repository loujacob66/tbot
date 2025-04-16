import requests

COINGECKO_API = "https://api.coingecko.com/api/v3"

def get_symbol_id_map():
    """Build a mapping of symbol → [coin IDs] from Coingecko."""
    try:
        response = requests.get(f"{COINGECKO_API}/coins/list")
        response.raise_for_status()
        data = response.json()

        symbol_map = {}
        for coin in data:
            symbol = coin["symbol"].lower()
            if symbol not in symbol_map:
                symbol_map[symbol] = []
            symbol_map[symbol].append(coin["id"])
        return symbol_map
    except Exception as e:
        print(f"Error building symbol map: {e}")
        return {}

def get_valid_token_ids(symbols, symbol_map):
    """Return the first valid token ID for each symbol (if known)."""
    result = {}
    for symbol in symbols:
        ids = symbol_map.get(symbol.lower())
        if ids:
            result[symbol.lower()] = ids[0]  # take the first match
    return result
