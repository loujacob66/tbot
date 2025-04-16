
from typer import Typer
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

app = Typer()

@app.command("top")
def top_tokens(since: str = "24h", limit: int = 10):
    db_path = Path(__file__).parent.parent / "logs" / "trending.db"
    if not db_path.exists():
        print("❌ No database found.")
        return

    if since.endswith("h"):
        hours = int(since.rstrip("h"))
        start_time = datetime.utcnow() - timedelta(hours=hours)
    elif since.endswith("d"):
        days = int(since.rstrip("d"))
        start_time = datetime.utcnow() - timedelta(days=days)
    else:
        print("⚠️ Use --since format like '24h' or '3d'")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT token,
               SUM(mentions) AS total_mentions,
               SUM(karma) AS total_karma,
               COUNT(DISTINCT timestamp) AS scan_count
        FROM tokens
        WHERE timestamp >= ?
        GROUP BY token
        ORDER BY total_karma DESC
        LIMIT ?
        """,
        (start_time.strftime("%Y-%m-%d_%H-%M-%S"), limit)
    )

    rows = cursor.fetchall()
    print(f"📊 Top {limit} tokens since {since}:\n")
    for token, mentions, karma, scans in rows:
        print(f"  • {token:10} — mentions: {mentions:<4} karma: {karma:<6} scans: {scans}")
    conn.close()
