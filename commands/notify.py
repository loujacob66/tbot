
from typer import Typer
from lib.notify import send_pushover_message

app = Typer()

@app.command("test")
def notify_test(title: str = "tbot Test", message: str = "This is a test message."):
    send_pushover_message(message, title)
    print("✅ Test alert sent.")
