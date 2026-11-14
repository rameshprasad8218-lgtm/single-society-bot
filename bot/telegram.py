import os, requests


def ready():
    return bool(os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"))


def send(png_path, caption):
    tok = os.environ["TELEGRAM_BOT_TOKEN"]
    chat = os.environ["TELEGRAM_CHAT_ID"].strip()
    if not chat.startswith("@") and not chat.lstrip("-").isdigit():
        chat = "@" + chat
    with open(png_path, "rb") as f:
        r = requests.post(
            f"https://api.telegram.org/bot{tok}/sendPhoto",
            data={"chat_id": chat, "caption": caption[:1024]},
            files={"photo": f},
            timeout=60,
        )
    if not r.ok:
        raise RuntimeError(f"Telegram {r.status_code}: {r.text[:200]}")
    return r.json()["result"]["message_id"]
