output "repository_name" {
  description = "Name of the ECR repository."
  value       = aws_ecr_repository.this.name
}

output "repository_url" {
  description = "Repository URL used for pushing container images."
  value       = aws_ecr_repository.this.repository_url
}