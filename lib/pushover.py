
import json
import requests
from pathlib import Path

def send_pushover(message: str):
    try:
        secrets_path = Path("config/pushover_secrets.json")
        if not secrets_path.exists():
            print("❌ Missing config/pushover_secrets.json")
            return

        with secrets_path.open() as f:
            secrets = json.load(f)

        token = secrets.get("app_token")
        user = secrets.get("user_key")

        if not token or not user:
            print("❌ Missing app_token or user_key in pushover_secrets.json")
            return

        response = requests.post("https://api.pushover.net/1/messages.json", data={
            "token": token,
            "user": user,
            "message": message
        })

        if response.status_code == 200:
            print("📲 Pushover alert sent")
        else:
            print(f"❌ Failed to send Pushover alert: {response.status_code} — {response.text}")

    except Exception as e:
        print(f"💥 Exception in send_pushover: {e}")
