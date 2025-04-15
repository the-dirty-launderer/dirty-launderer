
import os
import json
import requests
from google.auth import default
from googleapiclient.discovery import build

def send_alert(message):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("ALERT_CHAT_ID")
    if token and chat_id:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": chat_id, "text": f"⚠️ [Budget Alert] {message}"}
        )

def main(event, context):
    credentials, project_id = default()
    region = os.environ.get("REGION", "us-central1")

    send_alert("Shutdown triggered due to budget overage. Disabling services...")

    function_names = [
        "dirty-launderer-bot",
        "dirty-launderer-validate-proxies",
        "dirty-launderer-github-proxysync",
        "dirty-launderer-webhookcheck"
    ]

    try:
        functions = build("cloudfunctions", "v1", credentials=credentials)
        for name in function_names:
            fn_path = f"projects/{project_id}/locations/{region}/functions/{name}"
            try:
                functions.projects().locations().functions().delete(name=fn_path).execute()
                send_alert(f"✅ Deleted Cloud Function: {name}")
            except Exception as e:
                send_alert(f"⚠️ Could not delete function {name}: {e}")
    except Exception as e:
        send_alert(f"❌ Failed to shutdown Cloud Functions: {e}")

    try:
        scheduler = build("cloudscheduler", "v1", credentials=credentials)
        parent = f"projects/{project_id}/locations/{region}"
        jobs = scheduler.projects().locations().jobs().list(parent=parent).execute()
        for job in jobs.get("jobs", []):
            job["state"] = "PAUSED"
            scheduler.projects().locations().jobs().patch(name=job["name"], body=job).execute()
            send_alert(f"⏸️ Paused Scheduler job: {job['name']}")
    except Exception as e:
        send_alert(f"❌ Failed to pause Scheduler jobs: {e}")
