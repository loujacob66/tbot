import sqlite3
from pathlib import Path
from datetime import datetime

def show_latest_trends():
    db_path = Path(__file__).resolve().parent.parent / "logs" / "trending.db"
    if not db_path.exists():
        print(f"⚠️  No database found at: {db_path}")
        return

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Get the latest timestamp from the trends table
    cursor.execute("SELECT DISTINCT timestamp FROM trends ORDER BY timestamp DESC LIMIT 1")
    latest_ts_row = cursor.fetchone()
    if not latest_ts_row:
        print("⚠️  No entries found in the database.")
        return

    latest_ts = latest_ts_row[0]
    cursor.execute("SELECT symbol, price, mentions, score, timestamp FROM trends WHERE timestamp = ? ORDER BY score DESC", (latest_ts,))
    
    print(f"🕒 Most recent scan: {datetime.fromisoformat(latest_ts).strftime('%Y-%m-%d %H:%M:%S')}")
    for row in cursor.fetchall():
        print(f"{row[0]:<6} — Score: {row[3]:<8} — Mentions: {row[2]} — ${row[1]}")

    conn.close()

if __name__ == "__main__":
    show_latest_trends()
