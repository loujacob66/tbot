import csv
import json
import os
from datetime import datetime

def ensure_log_dir(log_dir="logs"):
    os.makedirs(log_dir, exist_ok=True)

def timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d_%H-%M")

def log_to_csv(filepath, data):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["symbol", "mentions", "price", "score"])
        for row in data:
            writer.writerow(row)

def log_to_json(filepath, data):
    json_data = [
        {"symbol": s, "mentions": m, "price": p, "score": sc}
        for s, m, p, sc in data
    ]
    with open(filepath, "w") as f:
        json.dump(json_data, f, indent=2)

def append_to_history(filepath, data):
    is_new = not os.path.exists(filepath)
    with open(filepath, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp", "symbol", "mentions", "price", "score"])
        ts = datetime.utcnow().isoformat()
        for symbol, mentions, price, score in data:
            writer.writerow([ts, symbol, mentions, price, score])
