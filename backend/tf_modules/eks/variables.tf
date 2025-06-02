variable "cluster_name" {
  description = "EKS Cluster name"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "eu-north-1"
}

variable "node_count" {
  description = "Number of nodes in the cluster"
  type        = number
  default     = 2
}