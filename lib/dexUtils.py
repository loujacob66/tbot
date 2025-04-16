
import random

# Mock function to simulate DEX volume enrichment
def get_dex_volumes(tokens: dict) -> dict:
    for token, data in tokens.items():
        data["dex_volume"] = round(random.uniform(0, 1000000), 2)
    return tokens
