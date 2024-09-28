variable "project_id" {
  description = "GCP Project ID"
}

variable "region" {
  description = "GCP Region"
  default     = "us-central1"
}

variable "db_instance_name" {
  description = "Cloud SQL instance name"
  default     = "my-db-instance"
}

variable "db_username" {
  description = "DB username"
  default     = "postgres"
}

variable "db_password" {
  description = "DB password"
}

variable "db_name" {
  description = "Database name"
  default     = "appdb"
}

variable "cloud_run_service_name" {
  description = "Cloud Run service name"
  default     = "backend-service"
}

variable "database_url" {
  description = "Database connection URL"
}
