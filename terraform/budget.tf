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
