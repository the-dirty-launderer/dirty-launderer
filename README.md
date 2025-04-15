[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


💃 *A lady in the streets, and clean in the sheets… of tracking parameters.* 🧼
[![CI Build](https://github.com/the-dirty-launderer/dirty-launderer/actions/workflows/python-tests.yml/badge.svg)](https://github.com/the-dirty-launderer/dirty-launderer/actions/workflows/python-tests.yml)
[![Docs](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://the-dirty-launderer.github.io/dirty-launderer)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](#)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Dirty Launderer 🧼

A privacy-first Telegram bot that automatically cleans tracking parameters from URLs, and proxies uncleanable links using services like Invidious, Nitter, Libreddit, and more.

## 🔧 Features

- Auto-cleans URLs from common trackers
- Supports proxying via privacy frontends
- Fully admin-configurable via Telegram commands
- PII-safe logging to Google Cloud Logging
- Modular domain handler design
- Cloud Functions + Firestore + Terraform + GitHub Actions

## 📦 Repo Structure

```
dirty-launderer/
├── bot/                  # Telegram bot source code
│   ├── main.py
│   ├── admin/            # Admin command handlers
│   ├── handlers/         # Domain-specific link handlers
│   ├── utils/            # Firestore + proxy helpers
├── terraform/            # Infrastructure as code (GCP)
│   ├── main.tf
│   ├── budget.tf
│   ├── github.tf
├── dist/                 # Deployment ZIP (autogenerated)
├── post_apply.sh         # Optional webhook registrar
├── .github/workflows/    # GitHub Actions
│   └── deploy.yml
├── README.md
```

## 🚀 Deployment

1. **Add secrets to GitHub**:
    - `GCP_CREDENTIALS`
    - `GCP_PROJECT_ID`
    - `TELEGRAM_BOT_TOKEN`
    - `ADMIN_CHAT_ID`
    - `GCS_BUCKET_NAME`

2. **Push to main branch** → GitHub Actions will:
    - Zip bot/
    - Upload to GCS
    - Run `terraform apply` from terraform/

3. **Webhook is auto-registered via post_apply.sh or Cloud Function**

## 🤖 Telegram Commands

Run `/setcommands` in BotFather and paste:

```
setdomain - Set handling for a specific domain
listdomains - View all domain rules
resetdomains - Reset domain settings to default
setdefault - Set default behavior for unknown domains
setlogging - Enable or disable safe logging
showlogging - View current logging mode
previewdomain - Preview handling for a domain
tools - Show admin tools
welcome - Show welcome/help message
ping - Check if the bot is running and webhook is healthy
alerttest - Test an admin alert
status - Check bot status and webhook info
proxies - Show count of active proxy frontends
configsummary - Show this group's domain config
commands - Show a full list of bot commands
```

## 💬 Credits

Made by [you], deployed serverlessly on GCP.
