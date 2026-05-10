variable "repository_name" {
  description = "Name of the ECR repository."
  type        = string
}

variable "max_image_count" {
  description = "Maximum number of images retained by lifecycle policy."
  type        = number
}

variable "tags" {
  description = "Common tags applied to ECR resources."
  type        = map(string)
}