import os
import telegram
from telegram import Update
from telegram.ext import CallbackContext
import requests

def status(update: Update, context: CallbackContext):
    token = os.environ.get("TELEGRAM_TOKEN")
    try:
        resp = requests.get(f"https://api.telegram.org/bot{token}/getWebhookInfo")
        data = resp.json()
        if data.get("ok"):
            webhook_url = data["result"].get("url", "No webhook set")
            message = f"✅ Bot is running.
🌐 Webhook URL: {webhook_url}"
        else:
            message = "⚠️ Could not verify webhook info."
    except Exception as e:
        message = f"❌ Error fetching webhook status: {e}"
    update.message.reply_text(message)