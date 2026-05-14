output "eks_cluster_role_arn" {
  description = "ARN of the EKS control plane IAM role."
  value       = aws_iam_role.eks_cluster_role.arn
}

output "eks_node_role_arn" {
  description = "ARN of the EKS managed node group IAM role."
  value       = aws_iam_role.eks_node_role.arn
}

output "eks_cluster_role_name" {
  description = "Name of the EKS control plane IAM role."
  value       = aws_iam_role.eks_cluster_role.name
}

output "eks_node_role_name" {
  description = "Name of the EKS managed node group IAM role."
  value       = aws_iam_role.eks_node_role.name
}

output "github_actions_role_arn" {
  description = "ARN of the GitHub Actions IAM role."
  value       = aws_iam_role.github_actions.arn
}

output "external_dns_role_arn" {
  description = "ARN of the ExternalDNS IAM role."
  value       = aws_iam_role.external_dns.arn
}

