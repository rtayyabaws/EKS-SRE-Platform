variable "aws_region" {
  description = "AWS region used for the EKS platform."
  type        = string
}

variable "project_name" {
  description = "Name used for platform resources."
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the platform VPC."
  type        = string
}

variable "availability_zones" {
  description = "Availability zones used across the VPC."
  type        = list(string)
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets used by load balancers."
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets used by EKS nodes."
  type        = list(string)
}

variable "cluster_name" {
  description = "Name of the EKS cluster."
  type        = string
}

variable "kubernetes_version" {
  description = "Kubernetes version for the EKS cluster."
  type        = string
}

variable "instance_types" {
  description = "EC2 instance types for the EKS managed node group."
  type        = list(string)
}

variable "node_desired_size" {
  description = "Desired number of EKS worker nodes."
  type        = number
}

variable "node_min_size" {
  description = "Minimum number of EKS worker nodes."
  type        = number
}

variable "node_max_size" {
  description = "Maximum number of EKS worker nodes."
  type        = number
}

variable "repository_name" {
  description = "ECR repository name for the application image."
  type        = string
}

variable "max_image_count" {
  description = "Maximum number of container images retained in ECR."
  type        = number
}

variable "domain_name" {
  description = "Root Route53 hosted zone domain."
  type        = string
}

variable "app_domain_name" {
  description = "Application subdomain managed by ExternalDNS."
  type        = string
}

variable "tags" {
  description = "Common tags applied to AWS resources."
  type        = map(string)
}

