variable "project_name" {
  description = "Name used for IAM resources."
  type        = string
}

variable "tags" {
  description = "Common tags applied to IAM resources."
  type        = map(string)
}