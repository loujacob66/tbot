from pathlib import Path
import json

def load_json(path: str | Path) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    with p.open("r") as f:
        return json.load(f)
