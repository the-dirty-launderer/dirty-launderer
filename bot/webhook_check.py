
import os
import requests

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
EXPECTED_WEBHOOK_URL = os.environ["EXPECTED_WEBHOOK_URL"]
ALERT_CHAT_ID = os.environ.get("ALERT_CHAT_ID")  # Optional

def send_alert(message):
    if ALERT_CHAT_ID:
        alert_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": ALERT_CHAT_ID,
            "text": f"🚨 [Dirty Launderer Webhook] {message}"
        }
        requests.post(alert_url, data=payload)

def main(request):
    try:
        get_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getWebhookInfo"
        response = requests.get(get_url)
        info = response.json()
        current_url = info.get("result", {}).get("url", "")

        if current_url != EXPECTED_WEBHOOK_URL:
            set_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook"
            set_resp = requests.post(set_url, data={"url": EXPECTED_WEBHOOK_URL})
            if set_resp.status_code == 200:
                send_alert(f"Webhook was missing or wrong and has been re-registered to: {EXPECTED_WEBHOOK_URL}")
                return "✅ Webhook re-registered", 200
            send_alert(f"❌ Failed to register webhook: {set_resp.text}")
            return f"❌ Failed to register: {set_resp.text}", 500

        return "✅ Webhook is up to date", 200

    except Exception as e:
        send_alert(f"❌ Error checking webhook: {str(e)}")
        return f"Error: {str(e)}", 500
