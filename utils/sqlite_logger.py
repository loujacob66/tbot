import sqlite3
from datetime import datetime
from pathlib import Path

def ensure_sqlite_schema(db_path="logs/trending.db"):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            price REAL,
            mentions INTEGER,
            score REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_to_sqlite(data, db_path="logs/trending.db"):
    ensure_sqlite_schema(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    now = datetime.utcnow().isoformat()
    rows = [(symbol, price, mentions, score, now) for (symbol, mentions, price, score) in data]
    cursor.executemany(
        "INSERT INTO trends (symbol, price, mentions, score, timestamp) VALUES (?, ?, ?, ?, ?)",
        rows
    )

    conn.commit()
    conn.close()
