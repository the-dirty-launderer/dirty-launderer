import os
import json
import requests
from google.auth import default
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Validate required environment variables
REQUIRED_ENV_VARS = ["TELEGRAM_TOKEN", "ALERT_CHAT_ID"]
for var in REQUIRED_ENV_VARS:
    if not os.environ.get(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")

def send_alert(message):
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("ALERT_CHAT_ID")
    if token and chat_id:
        try:
            requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data={"chat_id": chat_id, "text": f"⚠️ [Budget Alert] {message}"},
                timeout=10
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send alert: {e}")

def main(event, context):
    credentials, project_id = default()
    region = os.environ.get("REGION", "us-central1")

    send_alert("Shutdown triggered due to budget overage. Disabling services...")

    function_names = os.environ.get("FUNCTION_NAMES", "").split(",")
    if not function_names:
        logger.error("No Cloud Function names provided.")
        return

    try:
        functions = build("cloudfunctions", "v1", credentials=credentials)
        for name in function_names:
            fn_path = f"projects/{project_id}/locations/{region}/functions/{name}"
            try:
                logger.info(f"Deleting Cloud Function: {name}")
                functions.projects().locations().functions().delete(name=fn_path).execute()
                send_alert(f"✅ Deleted Cloud Function: {name}")
            except HttpError as e:
                send_alert(f"⚠️ HTTP error while deleting function {name}: {e}")
            except Exception as e:
                send_alert(f"⚠️ Could not delete function {name}: {e}")
    except Exception as e:
        send_alert(f"❌ Failed to shutdown Cloud Functions: {e}")

    try:
        scheduler = build("cloudscheduler", "v1", credentials=credentials)
        parent = f"projects/{project_id}/locations/{region}"
        jobs = scheduler.projects().locations().jobs().list(parent=parent).execute()
        for job in jobs.get("jobs", []):
            try:
                scheduler.projects().locations().jobs().pause(name=job["name"]).execute()
                send_alert(f"⏸️ Paused Scheduler job: {job['name']}")
            except Exception as e:
                send_alert(f"❌ Failed to pause Scheduler job {job['name']}: {e}")
    except Exception as e:
        send_alert(f"❌ Failed to pause Scheduler jobs: {e}")
