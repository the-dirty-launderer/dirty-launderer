
import os
import requests
from google.cloud import storage

GITHUB_URL = os.environ["GITHUB_PROXY_JSON_URL"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
DEST_PATH = os.environ.get("GCS_DEST_PATH", "proxies.json")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

def main(request):
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    try:
        resp = requests.get(GITHUB_URL, headers=headers)
        if resp.status_code != 200:
            return f"Failed to fetch from GitHub: {resp.status_code} {resp.text}", 500

        content = resp.text

        client = storage.Client()
        bucket = client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(DEST_PATH)
        blob.upload_from_string(content, content_type="application/json")

        return f"✅ Synced proxies.json to gs://{BUCKET_NAME}/{DEST_PATH}", 200

    except Exception as e:
        return f"❌ Sync error: {str(e)}", 500
