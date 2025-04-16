
import json
from pathlib import Path
from datetime import datetime
from lib.walletUtils import score_tokens_by_wallets
from lib.tokenPrices import get_prices
from lib.dexUtils import get_dex_volumes
from lib.redditFetcher import fetch_reddit_posts

def fetch_trending_tokens(limit=10):
    # Load config
    subreddits_path = Path("config/subreddits.json")
    blacklist_path = Path("config/blacklist.json")

    with subreddits_path.open() as f:
        subreddits = json.load(f)

    with blacklist_path.open() as f:
        blacklist = set([token.lower() for token in json.load(f)])

    # Fetch live Reddit data
    posts = fetch_reddit_posts()

    # Extract and count token mentions
    mentions = {}
    for post in posts:
        symbols = post.get("symbols", [])
        karma = post.get("score", 1)

        for symbol in symbols:
            symbol_lc = symbol.lower()
            if symbol_lc in blacklist:
                continue

            if symbol not in mentions:
                mentions[symbol] = {"symbol": symbol, "mentions": 0, "karma": 0}

            mentions[symbol]["mentions"] += 1
            mentions[symbol]["karma"] += karma

        # Get real prices
    prices = get_prices(list(mentions.keys()))

    # Build basic token data (before enrichment)
    results = []
    for data in mentions.values():
        symbol = data["symbol"]
        price = prices.get(symbol.upper(), 1.0)

        results.append({
            "symbol": symbol,
            "price": price,
            "mentions": data["mentions"],
            "karma": data["karma"],
            "wallet_score": 0.0,
            "dex_volume": 0.0,
            "score": 0.0  # temporary placeholder
        })

    # Enrich with wallet and DEX data
    symbol_map = {t["symbol"]: t for t in results}
    score_tokens_by_wallets(symbol_map)
    get_dex_volumes(symbol_map)

    # Recalculate final score with weights
    for token in results:
        token["score"] = (
            token["mentions"] * token["karma"]
            + token["wallet_score"] * 1000
            + token["dex_volume"] / 10000
        )
        token["score"] = round(token["score"], 2)

    return sorted(results, key=lambda x: x["score"], reverse=True)[:limit]


def mock_price_lookup(symbol):
    # Replace this with CoinGecko or another price feed later
    prices = {
        "ETH": 3200,
        "SOL": 155,
        "DOGE": 0.16,
        "SHIBA": 0.000025,
        "AVAX": 42,
        "FLOKI": 0.00018,
        "LDO": 2.6
    }
    return prices.get(symbol.upper(), 1.0)
