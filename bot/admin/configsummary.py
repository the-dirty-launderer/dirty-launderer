from telegram import Update
from telegram.ext import CallbackContext
from google.cloud import firestore

def configsummary(update: Update, context: CallbackContext):
    chat_id = str(update.effective_chat.id)
    db = firestore.Client()
    doc_ref = db.collection("group_config").document(chat_id)
    doc = doc_ref.get()

    if not doc.exists:
        update.message.reply_text("⚠️ No config found for this group.")
        return

    data = doc.to_dict()
    default_behavior = data.get("default_behavior", "clean")
    domain_rules = data.get("domain_rules", {})

    lines = [f"🛠️ Current Group Config:", f"Default behavior: {default_behavior}"]
    if domain_rules:
        lines.append("\nOverrides:")
        for domain, action in domain_rules.items():
            lines.append(f"- {domain}: {action}")
    else:
        lines.append("No domain-specific overrides configured.")

    update.message.reply_text("\n".join(lines))