
import json
from pathlib import Path

def load_blacklist(path=None):
    if path is None:
        path = Path("config/blacklist.json")
    if not path.exists():
        return set()
    with open(path, "r") as f:
        return set(json.load(f))
