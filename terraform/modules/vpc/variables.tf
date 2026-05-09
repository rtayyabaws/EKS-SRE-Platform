variable "project_name" {
  description = "Name used for platform networking resources."
  type        = string
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
}

variable "availability_zones" {
  description = "Availability zones used across public and private subnets."
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

variable "tags" {
  description = "Common tags applied to VPC resources."
  type        = map(string)
}