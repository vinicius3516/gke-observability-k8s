terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.46.0"
    }
  }

  backend "s3" {
    bucket       = "placeholder"
    key          = "placeholder"
    region       = "placeholder"
    encrypt      = true
    use_lockfile = true
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}