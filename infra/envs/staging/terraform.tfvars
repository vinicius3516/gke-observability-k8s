# VPC
subnet_cidr   = "10.0.0.0/24"
pods_cidr     = "10.1.0.0/16"
services_cidr = "10.2.0.0/16"

# GKE
master_cidr       = "172.16.0.0/28"
gke_num_nodes     = 2
min_node_count    = 1
max_node_count    = 5
machine_type      = "e2-medium"
disk_size_gb      = 50
preemptible_nodes = false