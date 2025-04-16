import json
from datetime import datetime
from pathlib import Path

def fetch_posts(limit=15):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    posts_path = Path(f"logs/posts_{timestamp}.json")

    # Simulated placeholder
    sample_post = {
        "id": "abc123",
        "subreddit": "CryptoCurrency",
        "title": "Sample token discussion ABC DEF GHI",
        "score": 1200,
        "upvote_ratio": 0.95,
        "created_utc": 1744610000.0,
        "num_comments": 35
    }
    posts = [sample_post] * limit

    posts_path.parent.mkdir(parents=True, exist_ok=True)
    with posts_path.open("w") as f:
        json.dump(posts, f, indent=2)

    return posts, timestamp