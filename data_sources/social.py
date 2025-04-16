import requests
import re
from collections import Counter, defaultdict
from data_sources.price import get_token_prices_batch
from data_sources.symbol_map import get_symbol_id_map, get_valid_token_ids

HEADERS = {"User-agent": "tbot"}

SUBREDDITS = [
    "CryptoCurrency",
    "CryptoMoonShots",
    "AltStreetBets",
    "CryptoMarkets",
    "SatoshiStreetBets",
]

SYMBOL_BLACKLIST = {
    "UP", "WOULD", "OVER", "KNOW", "HERE", "ME", "WE", "ST", "TIME", "MONEY", "BUY", "SELL",
    "FREE", "GAS", "JUST", "NOW", "NEW", "YOUR", "GET", "TOP", "DO", "CAN", "SEND", "MAKE",
    "LIKE", "ALL", "TO", "OF", "IN", "ON", "IT", "AT", "AS", "BY", "BE", "OR", "IS", "AN", "DO",
    "HTTPS", "HTTP", "WWW", "COM", "ANY", "IF", "CRYPTO", "REDDIT", "TRADE", "HOLD", "WIN",
    "HOT", "NEXT", "SOON", "FAST", "OWN", "MOON", "GROW", "BEST", "SAFE", "REAL", "TRY", "HOPE",
    "TRUST", "TRUE", "FUD", "PUMP", "NEWS", "BULL", "BEAR", "FOMO", "LOCK", "WALLET", "DROP",
    "LIST", "RANK", "TOKEN", "DEFI", "CASH", "BANK", "USD", "NFT", "AI", "AIRDROP"
}

SYMBOL_PATTERN = re.compile(r'\b[A-Z0-9]{2,10}\b')

def fetch_posts(subreddit, sort="top", time_filter="day", limit=100):
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}&t={time_filter}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.json().get("data", {}).get("children", [])
    except Exception as e:
        print(f"⚠️ Error fetching subreddit {subreddit}: {e}")
    return []

def extract_symbols(text):
    return SYMBOL_PATTERN.findall(text.upper())

def get_trending_tokens(limit=10):
    symbol_counts = defaultdict(float)
    posts_seen = 0

    for sub in SUBREDDITS:
        posts = fetch_posts(sub)
        for post in posts:
            post_data = post["data"]
            score = post_data.get("score", 1)
            text = f"{post_data.get('title', '')} {post_data.get('selftext', '')}"
            symbols = extract_symbols(text)

            for sym in symbols:
                if sym not in SYMBOL_BLACKLIST:
                    symbol_counts[sym] += 1 * score
            posts_seen += 1

    print(f"🔎 Scanned {posts_seen} posts from {len(SUBREDDITS)} subreddits")

    sorted_symbols = sorted(symbol_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    symbol_map = get_symbol_id_map()
    symbols = [s[0] for s in sorted_symbols]
    valid_ids = get_valid_token_ids(symbols, symbol_map)
    prices = get_token_prices_batch([symbol_map.get(s[0]) for s in sorted_symbols if symbol_map.get(s[0]) in valid_ids])

    result = []
    for sym, mentions in sorted_symbols:
        token_id = symbol_map.get(sym)
        if token_id in prices:
            price = prices[token_id]
            score = mentions * price
            result.append((sym, mentions, price, score))

    return result
