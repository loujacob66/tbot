
import requests
import json
from pathlib import Path
from datetime import datetime

def fetch_reddit_posts():
    subreddits_path = Path("config/subreddits.json")
    blacklist_path = Path("config/blacklist.json")

    with subreddits_path.open() as f:
        subreddits = json.load(f)

    with blacklist_path.open() as f:
        blacklist = set([t.lower() for t in json.load(f)])

    all_posts = []

    for subreddit in subreddits:
        url = f"https://www.reddit.com/r/{subreddit}/top.json?t=day&limit=25"
        headers = {"User-Agent": "tbot/1.0"}

        try:
            res = requests.get(url, headers=headers, timeout=10)
            res.raise_for_status()
            data = res.json()

            for item in data.get("data", {}).get("children", []):
                post = item["data"]
                title = post.get("title", "")
                score = post.get("score", 1)

                # Extract symbols using $SYMBOL or uppercase ticker-like patterns
                symbols = extract_symbols_from_title(title, blacklist)

                if symbols:
                    all_posts.append({
                        "title": title,
                        "score": score,
                        "symbols": symbols,
                        "subreddit": subreddit
                    })

        except Exception as e:
            print(f"⚠️ Error fetching /r/{subreddit}: {e}")

    return all_posts


def extract_symbols_from_title(title, blacklist):
    import re
    matches = set()

    # Match $TOKEN and uppercase tokens (2-6 chars)
    dollar_matches = re.findall(r'\$(\w{2,10})', title)
    upper_matches = re.findall(r'\b[A-Z]{2,6}\b', title)

    for symbol in dollar_matches + upper_matches:
        if symbol.lower() not in blacklist:
            matches.add(symbol.upper())

    return list(matches)
