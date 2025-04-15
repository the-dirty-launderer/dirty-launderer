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
  source_archive_object = "bot-source.zip"  # uploaded manually
  entry_point           = "main"
  trigger_http          = true

  environment_variables = {
    TELEGRAM_TOKEN = var.telegram_bot_token
    ADMIN_CHAT_ID  = var.admin_chat_id
  }
}
