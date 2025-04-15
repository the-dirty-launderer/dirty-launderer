
resource "google_cloudfunctions_function" "budget_shutdown" {
  name        = "budget-auto-shutdown"
  runtime     = "python311"
  region      = var.region
  source_archive_bucket = google_storage_bucket.bot_source_bucket.name
  source_archive_object = google_storage_bucket_object.bot_zip.name
  entry_point = "main"
  trigger_topic = google_pubsub_topic.budget_alert_topic.name

  environment_variables = {
    REGION = var.region
  }
}
