
from collections import defaultdict
from datetime import datetime
import time

def process_posts(posts, timestamp):
    processed_posts = []
    token_stats = defaultdict(lambda: {
        "total_mentions": 0,
        "unique_posts": 0,
        "total_karma": 0,
        "avg_karma_per_post": 0.0,
        "karma_per_minute_max": 0.0
    })

    for post in posts:
        created_utc = post.get("created_utc", time.time())
        age_minutes = max((time.time() - created_utc) / 60, 1)
        karma = post.get("score", 0)
        karma_per_minute = karma / age_minutes

        processed = {
            "id": post.get("id"),
            "subreddit": post.get("subreddit"),
            "title": post.get("title"),
            "karma": karma,
            "upvote_ratio": post.get("upvote_ratio", 0.0),
            "created_utc": created_utc,
            "num_comments": post.get("num_comments", 0),
            "post_age_minutes": round(age_minutes, 2),
            "karma_per_minute": round(karma_per_minute, 4),
            "mentions": post.get("mentions", [])
        }

        processed_posts.append(processed)

        for token in post.get("mentions", []):
            stats = token_stats[token]
            stats["total_mentions"] += 1
            stats["total_karma"] += karma
            stats["karma_per_minute_max"] = max(stats["karma_per_minute_max"], karma_per_minute)

    for token, stats in token_stats.items():
        stats["unique_posts"] = sum(1 for p in processed_posts if token in p["mentions"])
        if stats["unique_posts"] > 0:
            stats["avg_karma_per_post"] = round(stats["total_karma"] / stats["unique_posts"], 2)

    return {
        "posts": processed_posts,
        "tokens": token_stats
    }
