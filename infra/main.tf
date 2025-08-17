module "vpc" {
  source        = "git::https://github.com/Vinicius-DevOps/terrform-gpc-modules.git//modules/vpc?ref=main"
  environment   = var.environment
  subnet_cidr   = var.subnet_cidr
  region        = var.region
  pods_cidr     = var.pods_cidr
  services_cidr = var.services_cidr
}

module "gke" {
  source            = "git::https://github.com/Vinicius-DevOps/terrform-gpc-modules.git//modules/gke?ref=main"
  environment       = var.environment
  region            = var.region
  project_id        = var.project_id
  vpc_name          = module.vpc.vpc_name
  subnet_name       = module.vpc.subnet_name
  master_cidr       = var.master_cidr
  gke_num_nodes     = var.gke_num_nodes
  preemptible_nodes = var.preemptible_nodes
  machine_type      = var.machine_type
  disk_size_gb      = var.disk_size_gb
  min_node_count    = var.min_node_count
  max_node_count    = var.max_node_count
}