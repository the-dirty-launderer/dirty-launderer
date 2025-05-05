resource "google_billing_budget" "project_budget" {
  billing_account = var.billing_account_id
  display_name    = "${var.environment} Dirty Launderer Budget"

  budget_filter {
    projects = [var.project_id]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = var.budget_amount
    }
  }

  threshold_rules {
    threshold_percent = 0.8
  }

  threshold_rules {
    threshold_percent = 1.0
  }

  all_updates_rule {
    pubsub_topic   = google_pubsub_topic.budget_alert_topic.id
    schema_version = "1.0"
  }
}

resource "google_pubsub_topic" "budget_alert_topic" {
  name = "${var.environment}-budget-alert-topic"
}

resource "google_pubsub_subscription" "shutdown_trigger_sub" {
  name  = "${var.environment}-budget-trigger-sub"
  topic = google_pubsub_topic.budget_alert_topic.name
}

# Define a Pub/Sub topic for budget alerts
resource "google_pubsub_topic" "budget_alert_topic_main" {
  name = "budget-alert-topic-main"
}

# Define a Pub/Sub subscription for the budget alert topic
resource "google_pubsub_subscription" "budget_alert_subscription_main" {
  name  = "budget-alert-subscription-main"
  topic = google_pubsub_topic.budget_alert_topic_main.name
}

# Define a Cloud Function to process budget alerts
resource "google_cloudfunctions_function" "budget_alert_function" {
  name                  = "budget-alert-function"
  description           = "Processes budget alerts and sends notifications"
  runtime               = "python311"
  project               = var.project_id
  region                = var.region
  source_archive_bucket = var.GCS_BUCKET_NAME
  source_archive_object = "budget-alert.zip"
  entry_point           = "main"
  trigger_http          = false

  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = google_pubsub_topic.budget_alert_topic_main.id
  }

  environment_variables = {
    TELEGRAM_BOT_TOKEN = var.telegram_bot_token
    ADMIN_CHAT_ID      = var.admin_chat_id
  }
}

# Grant the Cloud Function permission to consume Pub/Sub messages
resource "google_project_iam_member" "alert_function_pubsub_invoker" {
  project = var.project_id
  role    = "roles/pubsub.subscriber"
  member  = "serviceAccount:${google_cloudfunctions_function.budget_alert_function.service_account_email}"
}
