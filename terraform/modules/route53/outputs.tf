output "zone_id" {
  description = "Route53 hosted zone ID."
  value       = data.aws_route53_zone.this.zone_id
}

output "zone_name" {
  description = "Route53 hosted zone name."
  value       = data.aws_route53_zone.this.name
}