
import requests
import time

def fetch_token_price_data(symbols):
    url = "https://api.coingecko.com/api/v3/simple/price"
    ids = ",".join(symbols)
    params = {
        "ids": ids,
        "vs_currencies": "usd",
        "include_market_cap": "true",
        "include_24hr_vol": "true"
    }

    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"⚠️ Failed to fetch prices: {resp.status_code}")
        except Exception as e:
            print(f"⚠️ Error fetching prices: {e}")
        time.sleep(2)

    return {}
