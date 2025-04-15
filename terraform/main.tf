
provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "bot_source_bucket" {
  name     = "${var.project_id}-dirty-launderer-source"
  location = var.region
}

resource "google_storage_bucket_object" "bot_zip" {
  name   = "dirty-launderer-webhook.zip"
  bucket = google_storage_bucket.bot_source_bucket.name
  source = var.source_archive
}

resource "google_secret_manager_secret" "bot_token_secret" {
  secret_id = "dirty-launderer-bot-token"
  replication { automatic = true }
}

resource "google_secret_manager_secret_version" "bot_token_secret_version" {
  secret      = google_secret_manager_secret.bot_token_secret.id
  secret_data = var.bot_token
}

resource "google_cloudfunctions2_function" "dirty_launderer_bot" {
  name     = "dirty-launderer-bot"
  location = var.region

  build_config {
    runtime     = "python311"
    entry_point = "app"
    source {
      storage_source {
        bucket = google_storage_bucket.bot_source_bucket.name
        object = google_storage_bucket_object.bot_zip.name
      }
    }
  }

  service_config {
    environment_variables = {
      TELEGRAM_TOKEN_SECRET = "dirty-launderer-bot-token"
    }
    secret_environment_variables {
      key     = "TELEGRAM_TOKEN"
      secret  = google_secret_manager_secret.bot_token_secret.id
      version = "latest"
    }
    timeout_seconds = 60
  }

  event_trigger {
    event_type     = "google.cloud.functions.v2.http.request"
    trigger_region = var.region
  }
}

output "webhook_url" {
  value = "https://${google_cloudfunctions2_function.dirty_launderer_bot.name}-${var.region}-a.run.app"
}
