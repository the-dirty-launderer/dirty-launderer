
resource "google_billing_budget" "project_budget" {
  billing_account = var.billing_account_id
  display_name    = "Dirty Launderer $1 Budget"

  budget_filter {
    projects = [var.project_id]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = 1
    }
  }

  threshold_rules {
    threshold_percent = 0.8
  }

  threshold_rules {
    threshold_percent = 1.0
  }

  all_updates_rule {
    pubsub_topic = google_pubsub_topic.budget_alert_topic.id
    schema_version = "1.0"
  }
}

resource "google_pubsub_topic" "budget_alert_topic" {
  name = "budget-alert-topic"
}

resource "google_pubsub_subscription" "shutdown_trigger_sub" {
  name  = "budget-trigger-sub"
  topic = google_pubsub_topic.budget_alert_topic.name
}
