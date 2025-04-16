
import re
import json
from pathlib import Path
from lib.walletUtils import score_tokens_by_wallets
from lib.dexUtils import fetch_token_dex_volume

def extract_token_mentions(posts):
    pattern = re.compile(r'\b[A-Z]{2,5}\b')
    tokens = {}

    for post in posts:
        mentions = pattern.findall(post["title"])
        post["mentions"] = mentions
        for token in mentions:
            token = token.upper()
            if token not in tokens:
                tokens[token] = {
                    "total_mentions": 0,
                    "unique_posts": 0,
                    "total_karma": 0,
                    "avg_karma_per_post": 0,
                    "karma_per_minute_max": 0,
                    "dex_volume_usd": None,
                    "wallet_score": None,
                }
            tokens[token]["total_mentions"] += 1
            tokens[token]["unique_posts"] += 1
            tokens[token]["total_karma"] += post["score"]
            tokens[token]["karma_per_minute_max"] = max(
                tokens[token]["karma_per_minute_max"], post.get("karma_per_minute", 0)
            )

    for token, data in tokens.items():
        data["avg_karma_per_post"] = data["total_karma"] / max(data["unique_posts"], 1)

    return {
        "tokens": tokens,
        "posts": posts,
    }

def enrich_with_prices(tokens, token_price_data):
    for token, data in tokens.items():
        if token in token_price_data:
            data["price_usd"] = token_price_data[token].get("price_usd")
            data["market_cap"] = token_price_data[token].get("market_cap")
            data["volume_24h"] = token_price_data[token].get("volume_24h")
    return tokens

def enrich_with_wallet_and_dex(tokens):
    tokens = score_tokens_by_wallets(tokens)
    tokens = fetch_token_dex_volume(tokens)
    return tokens
