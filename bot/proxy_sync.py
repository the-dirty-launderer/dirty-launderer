import json
from proxy_helper import validate_all_proxies, write_to_firestore
import os
import telegram

def sync_and_validate_proxies(request):
    validated = validate_all_proxies()
    write_to_firestore(validated)

    all_down = all(len(lst) == 0 for lst in validated.values())
    if all_down:
        token = os.environ.get("TELEGRAM_TOKEN")
        bot = telegram.Bot(token=token)
        bot.send_message(chat_id=os.environ.get("ADMIN_CHAT_ID"), text="⚠️ All proxy instances failed validation!")

    return ("Proxy list validated and stored in Firestore.", 200)