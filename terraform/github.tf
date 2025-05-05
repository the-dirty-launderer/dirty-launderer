resource "google_cloudfunctions2_function" "github_proxy_sync" {
  name     = "github-proxy-sync"
  location = var.region
  project  = var.project_id

  build_config {
    runtime     = "python311"
    entry_point = "main"
    source {
      storage_source {
        bucket = var.GCS_BUCKET_NAME
        object = var.github_proxy_sync_source
      }
    }
  }

  service_config {
    environment_variables = {
      PROJECT_ID              = var.project_id
      BUCKET_NAME             = var.GCS_BUCKET_NAME
      GITHUB_PROXY_JSON_URL   = var.github_proxy_json_url
      GITHUB_TOKEN            = var.github_token
    }
    timeout_seconds  = 60
    available_memory = "256M"
  }
}

resource "google_cloudfunctions2_function_iam_member" "invoker" {
  project        = var.project_id
  location       = var.region
  cloud_function = google_cloudfunctions2_function.github_proxy_sync.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers" # Replace with a specific service account if needed
}