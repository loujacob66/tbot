import csv
import json

def log_trending_tokens_to_csv(filepath, data):
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["symbol", "mentions", "price", "score"])
        for row in data:
            writer.writerow(row)

def log_trending_tokens_to_json(filepath, data):
    json_data = [
        {"symbol": s, "mentions": m, "price": p, "score": sc}
        for s, m, p, sc in data
    ]
    with open(filepath, "w") as f:
        json.dump(json_data, f, indent=2)
