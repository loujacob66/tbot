from pathlib import Path
import csv
import sqlite3

def log_scan_results(results, timestamp):
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    posts_file = logs_dir / f"posts_{timestamp}.json"
    tokens_file = logs_dir / f"tokens_{timestamp}.json"
    history_file = logs_dir / "token_history.csv"

    # Save posts and tokens to JSON for traceability
    import json
    with open(posts_file, "w") as f:
        json.dump(results["posts"], f, indent=2)
    with open(tokens_file, "w") as f:
        json.dump(results["tokens"], f, indent=2)

    # Save token history to CSV
    with open(history_file, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for token, data in results["tokens"].items():
            writer.writerow([
                timestamp,
                token,
                data.get("total_mentions", 0),
                data.get("unique_posts", 0),
                data.get("total_karma", 0),
                data.get("avg_karma_per_post", 0),
                data.get("karma_per_minute_max", 0),
                data.get("dex_volume_usd", ""),
                data.get("wallet_score", "")
            ])

def log_tokens_to_db(tokens, timestamp):
    db_path = Path("logs") / "trending.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("DROP TABLE IF EXISTS tokens")
    c.execute("""
        CREATE TABLE IF NOT EXISTS tokens (
            timestamp TEXT,
            token TEXT,
            total_mentions INTEGER,
            unique_posts INTEGER,
            total_karma INTEGER,
            avg_karma_per_post REAL,
            karma_per_minute_max REAL,
            dex_volume_usd REAL,
            wallet_score REAL
        )
    """)

    for token, data in tokens.items():
        c.execute("""
            INSERT INTO tokens VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            token,
            data.get("total_mentions", 0),
            data.get("unique_posts", 0),
            data.get("total_karma", 0),
            data.get("avg_karma_per_post", 0),
            data.get("karma_per_minute_max", 0),
            data.get("dex_volume_usd", None),
            data.get("wallet_score", None)
        ))

    conn.commit()
    conn.close()