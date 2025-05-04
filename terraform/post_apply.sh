#!/bin/bash

# Set the Telegram bot webhook URL using output from Terraform

# Load outputs from Terraform (assumes you're in the terraform directory)
WEBHOOK_URL=$(terraform output -raw webhook_url)
BOT_TOKEN=$(terraform output -raw bot_secret_token)

# Register the webhook with Telegram
echo "Registering webhook with Telegram..."
curl -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" -d "url=${WEBHOOK_URL}"
echo -e "\n✅ Webhook registered: $WEBHOOK_URL"

variable "bot_source_archive" {
  description = "The name of the source archive object for the bot function"
  type        = string
  default     = "bot-source.zip"
}

variable "telegram_bot_token" {
  description = "The Telegram bot token"
  type        = string
}

variable "admin_chat_id" {
  description = "The Telegram chat ID for admin notifications"
  type        = string
}
