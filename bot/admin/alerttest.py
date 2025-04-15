import os
from telegram import Update
from telegram.ext import CallbackContext

def alerttest(update: Update, context: CallbackContext):
    from telegram import Bot
    bot = Bot(token=os.environ.get("TELEGRAM_TOKEN"))
    admin_chat_id = os.environ.get("ADMIN_CHAT_ID")

    try:
        bot.send_message(chat_id=admin_chat_id, text="✅ This is a test alert from Dirty Launderer.")
        update.message.reply_text("✅ Alert sent to admin chat ID.")
    except Exception as e:
        update.message.reply_text(f"❌ Failed to send alert: {e}")