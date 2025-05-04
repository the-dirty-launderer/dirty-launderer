resource "google_cloudfunctions_function" "budget_shutdown" {
  name                  = "budget-shutdown"
  description           = "Shuts down resources if budget is exceeded"
  runtime               = "python311"
  project               = var.project_id
  region                = var.region
  source_archive_bucket = var.GCS_BUCKET_NAME
  source_archive_object = var.source_archive_object
  entry_point           = "main"
  trigger_http          = true

  # Environment variables for the function
  environment_variables = {
    TELEGRAM_TOKEN        = var.telegram_token
    ALERT_CHAT_ID         = var.alert_chat_id
    EXPECTED_WEBHOOK_URL  = var.expected_webhook_url
  }

  # Function resource limits
  timeout            = 60
  available_memory_mb = 256
}

# IAM permissions to allow invocation of the Cloud Function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project_id
  region         = var.region
  cloud_function = google_cloudfunctions_function.budget_shutdown.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers" # Replace with a specific service account if needed
}