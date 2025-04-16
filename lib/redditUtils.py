
import praw
import json
import re
from pathlib import Path
from lib.tokenValidator import load_token_index, validate_mentions

def extract_token_mentions(text):
    matches = re.findall(r'\$(\w+)', text)
    return [token.upper() for token in matches]

def fetch_top_posts(subreddits, limit_per_sub=10):
    creds = json.loads((Path(__file__).parent.parent / "config" / "reddit_secrets.json").read_text())
    reddit = praw.Reddit(
        client_id=creds["client_id"],
        client_secret=creds["client_secret"],
        user_agent=creds["user_agent"],
    )

    token_index = load_token_index()

    posts = []
    for sub in subreddits:
        try:
            for post in reddit.subreddit(sub).top(time_filter="day", limit=limit_per_sub):
                mentions = extract_token_mentions(post.title)
                mentions = validate_mentions(mentions, token_index)
                posts.append({
                    "id": post.id,
                    "subreddit": sub,
                    "title": post.title,
                    "score": post.score,
                    "upvote_ratio": post.upvote_ratio,
                    "created_utc": post.created_utc,
                    "num_comments": post.num_comments,
                    "mentions": mentions,
                })
        except Exception as e:
            print(f"⚠️ Skipping subreddit {sub} — {e}")
            continue

    return posts
