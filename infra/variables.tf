# Global
variable "project_id" {
  description = "GCP project ID"
  type        = string
}
variable "environment" {
  description = "Environment name"
  type        = string
}
variable "region" {
  description = "GCP region"
  type        = string
}

# VPC
variable "subnet_cidr" {
  description = "Subnet CIDR"
  type        = string
}
variable "pods_cidr" {
  description = "Pods CIDR"
  type        = string
}
variable "services_cidr" {
  description = "Services CIDR"
  type        = string
}

# GKE
variable "master_cidr" {
  description = "Master CIDR"
  type        = string
}
variable "gke_num_nodes" {
  description = "Number of nodes"
  type        = number
}
variable "preemptible_nodes" {
  description = "Preemptible nodes"
  type        = bool
}
variable "machine_type" {
  description = "Machine type"
  type        = string
}
variable "disk_size_gb" {
  description = "Disk size in GB"
  type        = number
}
variable "min_node_count" {
  description = "Minimum number of nodes"
  type        = number
}
variable "max_node_count" {
  description = "Maximum number of nodes"
  type        = number
}