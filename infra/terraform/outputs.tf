output "frontend_bucket_name" {
  value = aws_s3_bucket.frontend.bucket
}

output "frontend_distribution_id" {
  value = aws_cloudfront_distribution.frontend.id
}

output "frontend_url" {
  value = "https://${local.frontend_fqdn}"
}

output "api_url" {
  value = "https://${local.api_fqdn}"
}

output "api_ecr_repository_url" {
  value = aws_ecr_repository.api.repository_url
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  value = aws_ecs_service.api.name
}

output "nat_gateway_public_ip" {
  value = aws_eip.nat.public_ip
}
