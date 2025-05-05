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
REQUIRED_ENV_VARS = ["TELEGRAM_TOKEN", "ALERT_CHAT_ID", "REGION", "FUNCTION_NAMES"]
for var in REQUIRED_ENV_VARS:
    if not os.environ.get(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")

def send_alert(message):
    """
    Sends an alert message to the configured Telegram chat.

    Args:
        message (str): The message to send.
    """
    token = os.environ.get("TELEGRAM_TOKEN")
    chat_id = os.environ.get("ALERT_CHAT_ID")
    if token and chat_id:
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{token}/sendMessage",
                data={"chat_id": chat_id, "text": f"⚠️ [Budget Alert] {message}"},
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send alert: {e}")

def delete_cloud_functions(credentials, project_id, region, function_names):
    """
    Deletes specified Cloud Functions.

    Args:
        credentials: Google Cloud credentials.
        project_id (str): The GCP project ID.
        region (str): The region where the functions are deployed.
        function_names (list): List of Cloud Function names to delete.
    """
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

def pause_scheduler_jobs(credentials, project_id, region):
    """
    Pauses all Cloud Scheduler jobs in the specified region.

    Args:
        credentials: Google Cloud credentials.
        project_id (str): The GCP project ID.
        region (str): The region where the jobs are deployed.
    """
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

def main(event, context):
    """
    Main function triggered by a budget alert. Deletes Cloud Functions and pauses Scheduler jobs.

    Args:
        event: The event payload (unused).
        context: Metadata for the event (unused).
    """
    credentials, project_id = default()
    region = os.environ.get("REGION", "us-central1")
    function_names = os.environ.get("FUNCTION_NAMES", "").split(",")

    if not function_names or function_names == [""]:
        logger.error("No Cloud Function names provided.")
        send_alert("❌ No Cloud Function names provided. Aborting shutdown.")
        return

    send_alert("🚨 Shutdown triggered due to budget overage. Disabling services...")

    # Delete Cloud Functions
    delete_cloud_functions(credentials, project_id, region, function_names)

    # Pause Scheduler Jobs
    pause_scheduler_jobs(credentials, project_id, region)

# In main.tf
resource "google_cloudfunctions_function_iam_member" "invoker_main" {
  project        = var.project_id
  region         = var.region
  cloud_function = google_cloudfunctions_function.dirty_launderer_bot.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers"
}
