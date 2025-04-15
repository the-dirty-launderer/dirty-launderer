
resource "google_cloudfunctions2_function" "github_proxy_sync" {
  name     = "dirty-launderer-github-proxysync"
  location = var.region

  build_config {
    runtime     = "python311"
    entry_point = "main"
    source {
      storage_source {
        bucket = google_storage_bucket.bot_source_bucket.name
        object = google_storage_bucket_object.bot_zip.name
      }
    }
  }

  service_config {
    environment_variables = {
      GITHUB_PROXY_JSON_URL = var.github_proxy_json_url
      BUCKET_NAME           = google_storage_bucket.bot_source_bucket.name
      GCS_DEST_PATH         = var.gcs_dest_path
      GITHUB_TOKEN          = var.github_token
    }
    timeout_seconds = 30
  }

  event_trigger {
    event_type     = "google.cloud.functions.v2.http.request"
    trigger_region = var.region
  }
}

resource "google_cloud_scheduler_job" "sync_proxy_json_job" {
  name        = "sync-github-proxies"
  description = "Sync proxies.json from GitHub every 24h"
  schedule    = "0 3 * * *"
  time_zone   = "Etc/UTC"

  http_target {
    uri        = "https://${google_cloudfunctions2_function.github_proxy_sync.name}-${var.region}-a.run.app"
    http_method = "GET"
  }
}
