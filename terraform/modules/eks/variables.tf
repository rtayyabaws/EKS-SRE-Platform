variable "cluster_name" {
  description = "Name of the EKS cluster."
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version used by EKS."
  type        = string
}

variable "cluster_role_arn" {
  description = "IAM role ARN for the EKS control plane."
  type        = string
}

variable "node_role_arn" {
  description = "IAM role ARN for the EKS managed node group."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs used by EKS worker nodes."
  type        = list(string)
}

variable "instance_types" {
  description = "EC2 instance types used by the managed node group."
  type        = list(string)
}

variable "node_desired_size" {
  description = "Desired number of worker nodes."
  type        = number
}

variable "node_min_size" {
  description = "Minimum number of worker nodes."
  type        = number
}

variable "node_max_size" {
  description = "Maximum number of worker nodes."
  type        = number
}

variable "tags" {
  description = "Common tags applied to EKS resources."
  type        = map(string)
}