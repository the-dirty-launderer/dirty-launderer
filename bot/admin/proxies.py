from telegram import Update
from telegram.ext import CallbackContext
from google.cloud import firestore

def proxies(update: Update, context: CallbackContext):
    db = firestore.Client()
    doc_ref = db.collection("validated_proxies").document("active")
    doc = doc_ref.get()

    if not doc.exists:
        update.message.reply_text("❌ No validated proxies available.")
        return

    proxies = doc.to_dict()
    lines = ["🛡️ Active Proxy Frontends:"]
    for service, urls in proxies.items():
        lines.append(f"- {service.capitalize()}: {len(urls)}")

    update.message.reply_text("\n".join(lines))