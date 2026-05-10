variable "aws_region" {
  description = "AWS region used for Terraform backend resources."
  type        = string
}

variable "state_bucket_name" {
  description = "S3 bucket name used for Terraform remote state."
  type        = string
}

variable "tags" {
  description = "Common tags applied to backend resources."
  type        = map(string)
}