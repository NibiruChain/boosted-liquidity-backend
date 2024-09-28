# Configure the Google provider
provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
}

# Create a VPC network
resource "google_compute_network" "network" {
  name = "my-vpc-network"
}

# Create a subnetwork
resource "google_compute_subnetwork" "subnetwork" {
  name          = "my-subnetwork"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.network.id
}

# Create a Serverless VPC Access Connector
resource "google_vpc_access_connector" "connector" {
  name          = "serverless-connector"
  region        = var.region
  network       = google_compute_network.network.id
  ip_cidr_range = "10.8.0.0/28"
}

# Create a Cloud SQL instance
resource "google_sql_database_instance" "db_instance" {
  name             = var.db_instance_name
  database_version = "POSTGRES_13"
  region           = var.region

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      # Private IP configuration
      private_network = google_compute_network.network.id
    }
  }
}

# Create a PostgreSQL user
resource "google_sql_user" "db_user" {
  name     = var.db_username
  instance = google_sql_database_instance.db_instance.name
  password = var.db_password
}

# Create a PostgreSQL database
resource "google_sql_database" "db" {
  name     = var.db_name
  instance = google_sql_database_instance.db_instance.name
}

# Service Account for Cloud Run
resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-sa"
  display_name = "Cloud Run Service Account"
}

# Grant necessary roles to the service account
resource "google_project_iam_member" "cloudsql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# IAM binding to allow Cloud Run Invoker
resource "google_cloud_run_service_iam_member" "invoker" {
  location = var.region
  service  = google_cloud_run_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Deploy the Cloud Run service with a placeholder image
resource "google_cloud_run_service" "backend" {
  name     = var.cloud_run_service_name
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/cloudrun/hello" # Placeholder image

        env {
          name  = "DATABASE_URL"
          value = var.database_url
        }
      }
      service_account_name = google_service_account.cloud_run_sa.email
    }

    metadata {
      annotations = {
        "run.googleapis.com/vpc-access-connector" = google_vpc_access_connector.connector.id
        "run.googleapis.com/vpc-access-egress"    = "all"
        "run.googleapis.com/cloudsql-instances"   = google_sql_database_instance.db_instance.connection_name
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_vpc_access_connector.connector]
}
