
variable "billing_account_id" {
  type        = string
  description = "GCP Billing Account ID"
}

variable "project_id" {
  type        = string
  description = "Your GCP project ID"
}

variable "region" {
  type        = string
  default     = "us-central1"
}
