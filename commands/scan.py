
import typer
from pathlib import Path
import json
import sqlite3
from datetime import datetime
from lib.notify import notify_if_enabled
from lib.tokenScanner import fetch_trending_tokens

app = typer.Typer()

@app.command()
def main(
    limit: int = 10,
    pushover: bool = False,
    log_json: bool = False,
    log_csv: bool = False,
    log_sqlite: bool = False
):
    print("🚀 scan.main() was called")

    tokens = fetch_trending_tokens(limit=limit)
    timestamp = datetime.utcnow().isoformat(timespec="seconds")

    try:
        for t in tokens:
            print(f"{t['symbol']: <6} — ${t['price']} — {t['mentions']} mentions — "
                  f"score: {t['score']:.2f} — wallet_score: {t['wallet_score']} — dex_volume: {t['dex_volume']}")

        Path("logs").mkdir(exist_ok=True)

        if log_json:
            with open("logs/latest.json", "w") as f:
                json.dump(tokens, f, indent=2)
            print("📝 Logged to logs/latest.json")

        if log_csv:
            with open("logs/latest.csv", "w") as f:
                f.write("symbol,price,mentions,score,wallet_score,dex_volume\n")
                for t in tokens:
                    f.write(f"{t['symbol']},{t['price']},{t['mentions']},{t['score']},{t['wallet_score']},{t['dex_volume']}\n")
            print("📝 Logged to logs/latest.csv")

            with open("logs/history.csv", "a") as f:
                for t in tokens:
                    f.write(f"{timestamp},{t['symbol']},{t['price']},{t['mentions']},{t['score']},{t['wallet_score']},{t['dex_volume']}\n")
            print("📈 Appended to logs/history.csv")

        if log_sqlite:
            conn = sqlite3.connect("logs/trending.db")
            c = conn.cursor()

            c.execute("""
                CREATE TABLE IF NOT EXISTS trending_tokens (
                    symbol TEXT,
                    price REAL,
                    mentions INTEGER,
                    score REAL,
                    wallet_score REAL,
                    dex_volume INTEGER
                )
            """)
            c.executemany(
                "INSERT INTO trending_tokens VALUES (?, ?, ?, ?, ?, ?)",
                [(t["symbol"], t["price"], t["mentions"], t["score"], t["wallet_score"], t["dex_volume"]) for t in tokens]
            )

            c.execute("""
                CREATE TABLE IF NOT EXISTS timestamped_scans (
                    timestamp TEXT,
                    symbol TEXT,
                    price REAL,
                    mentions INTEGER,
                    score REAL,
                    wallet_score REAL,
                    dex_volume INTEGER
                )
            """)
            c.executemany(
                "INSERT INTO timestamped_scans VALUES (?, ?, ?, ?, ?, ?, ?)",
                [(timestamp, t["symbol"], t["price"], t["mentions"], t["score"], t["wallet_score"], t["dex_volume"]) for t in tokens]
            )

            conn.commit()
            conn.close()
            print("📊 Logged to logs/trending.db (both tables)")

        class Args:
            def __init__(self, pushover):
                self.pushover = pushover

        notify_if_enabled("✅ Scan complete", Args(pushover))

    except Exception as e:
        print(f"💥 Exception occurred in scan: {e}")
