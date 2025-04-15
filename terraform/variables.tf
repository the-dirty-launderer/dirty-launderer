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
