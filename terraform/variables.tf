variable "telegram_bot_token" {
  description = "Telegram bot token from BotFather"
  type        = string
}

variable "admin_chat_id" {
  description = "Telegram admin user or group chat ID"
  type        = string
}

variable "project_id" {
  description = "Google Cloud project ID"
  type        = string
}

variable "billing_account_id" {
  description = "Google Cloud billing account ID (for budget automation)"
  type        = string
}

variable "region" {
  description = "Region to deploy resources (default: us-central1)"
  type        = string
  default     = "us-central1"
}

variable "source_archive" {
  description = "Path to the ZIP file in GCS (e.g., dist/bot-source.zip)"
  type        = string
}

variable "GCS_BUCKET_NAME" {
  description = "The name of the GCS bucket used to store the bot ZIP"
  type        = string
}

variable "bot_source_archive" {
  description = "The name of the source archive object for the bot function"
  type        = string
  default     = "bot-source.zip"
}

variable "github_proxy_sync_source" {
  description = "The name of the source archive object for the GitHub proxy sync function"
  type        = string
  default     = "github-proxy-sync.zip"
}

variable "github_proxy_json_url" {
  description = "The URL of the GitHub JSON file containing proxy information"
  type        = string
}

variable "github_token" {
  description = "The GitHub token for accessing private repositories"
  type        = string
}

variable "budget_amount" {
  description = "The budget amount in USD"
  type        = number
  default     = 1
}

variable "expected_webhook_url" {
  description = "Expected webhook URL for the Telegram bot"
  type        = string
}

variable "environment" {
  description = "The environment (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}