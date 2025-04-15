from telegram import Update
from telegram.ext import CallbackContext

def welcome(update: Update, context: CallbackContext):
    message = """👋 Welcome to Dirty Launderer — your privacy-first link cleaner bot.

🧼 This bot removes tracking parameters from URLs and can proxy uncleanable links via privacy frontends like Invidious, Nitter, Libreddit, and more.

🔧 Admin Commands:
/setdomain - Set handling for a specific domain
/listdomains - View all domain rules
/resetdomains - Reset domain settings to default
/setdefault - Set default behavior for unknown domains
/setlogging - Enable or disable safe logging
/showlogging - View current logging mode
/previewdomain - Preview handling for a domain
/tools - Show admin tools
/alerttest - Test an admin alert
/ping - Check if the bot is running and webhook is healthy
/welcome - Show this message

👁️ By default, tracking links are auto-cleaned or redirected. Configure behavior per group via these commands."""

    message += "\n\n💃 A lady in the streets, and clean in the sheets… of tracking parameters. 🧼"
    update.message.reply_text(message)