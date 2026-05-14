variable "project_name" {
  description = "Name used for IAM resources."
  type        = string
}

variable "tags" {
  description = "Common tags applied to IAM resources."
  type        = map(string)
}

variable "github_actions_role_arn" {
  description = "IAM role ARN for GitHub Actions — needs cluster access for destroy pipeline"
  type        = string
}