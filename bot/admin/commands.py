from telegram import Update
from telegram.ext import CallbackContext

def show_commands(update: Update, context: CallbackContext) -> None:
    """Show all available commands."""
    message = """📖 The Dirty Launderer🧼 Command Reference

🔧 Admin Controls:
/setdomain - Set handling for a specific domain
/listdomains - View all domain rules
/resetdomains - Reset domain settings
/setdefault - Set default domain behavior
/setlogging - Enable or disable safe logging
/showlogging - View current logging mode
/configsummary - Show this group's domain config

🛠️ Tools:
/previewdomain - Preview how a domain will be handled
/tools - Show admin tools
/alerttest - Send test alert to admin
/status - Check bot + webhook health
/proxies - Show count of active proxy frontends
/ping - Basic bot ping
/welcome - Show welcome/help message

Made with 🧼 by The Dirty Launderer🧼 team
"""
    # Ensure no identifiable information is logged
    update.message.reply_text(message)