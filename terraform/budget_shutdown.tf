resource "google_cloudfunctions_function" "budget_shutdown" {
  name                  = "budget-shutdown"
  description           = "Shuts down resources if the budget is exceeded"
  runtime               = "python311"
  project               = var.project_id
  region                = var.region
  source_archive_bucket = var.GCS_BUCKET_NAME
  source_archive_object = var.budget_shutdown_source
  entry_point           = "main"
  trigger_http          = true

  # Environment variables for the function
  environment_variables = {
    TELEGRAM_TOKEN  = var.telegram_bot_token
    ALERT_CHAT_ID   = var.alert_chat_id
    REGION          = var.region
    FUNCTION_NAMES  = var.function_names
  }

  # Function resource limits
  timeout            = 60
  available_memory_mb = 256
}

# IAM permissions to allow invocation of the Cloud Function
resource "google_cloudfunctions_function_iam_member" "invoker_budget_shutdown" {
  project        = var.project_id
  region         = var.region
  cloud_function = google_cloudfunctions_function.budget_shutdown.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers" # Replace with a specific service account if needed
}

# Pub/Sub topic for budget alerts
resource "google_pubsub_topic" "budget_alert_topic" {
  name = "${var.environment}-budget-alert-topic"
}

# Pub/Sub subscription for triggering the budget shutdown function
resource "google_pubsub_subscription" "budget_shutdown_trigger" {
  name  = "${var.environment}-budget-shutdown-trigger"
  topic = google_pubsub_topic.budget_alert_topic.name

  push_config {
    push_endpoint = google_cloudfunctions_function.budget_shutdown.https_trigger_url
  }
}