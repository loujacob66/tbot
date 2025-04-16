def notify_if_enabled(message, args=None):
    if args and getattr(args, "pushover", False):
        from .pushover import send_pushover
        send_pushover(message)
