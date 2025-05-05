provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_secret_manager_secret" "bot_token_secret" {
  secret_id = "telegram-bot-token"
  project   = var.project_id

  replication {
    user_managed {
      replicas {
        location = var.region
      }
      replicas {
        location = "us-central1" # Add additional replicas for high availability
      }
    }
  }
}

resource "google_secret_manager_secret_version" "bot_token_secret_version" {
  secret      = google_secret_manager_secret.bot_token_secret.id
  secret_data = var.telegram_bot_token
}

resource "google_cloudfunctions_function" "dirty_launderer_bot" {
  name        = "dirty-launderer-bot"
  description = "Telegram bot to clean URLs and proxy through privacy frontends"
  runtime     = "python311"
  project     = var.project_id
  region      = var.region

  source_archive_bucket = var.GCS_BUCKET_NAME
  source_archive_object = var.bot_source_archive
  entry_point           = "main"
  trigger_http          = true

  environment_variables = {
    TELEGRAM_TOKEN = var.telegram_bot_token
    ADMIN_CHAT_ID  = var.admin_chat_id
  }

  timeout            = 60
  available_memory_mb = 256
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project_id
  region         = var.region
  cloud_function = google_cloudfunctions_function.dirty_launderer_bot.name
  role           = "roles/cloudfunctions.invoker"
  member         = "allUsers" # Replace with a specific service account if needed
}
