# Beacon Terraform

This stack provisions:

- VPC with 2 public and 2 private subnets
- NAT Gateway with Elastic IP
- ECR repository for the API image
- ECS Fargate cluster, task definition, and service
- ALB and Route53 record for `api.beacon.<domain>`
- S3 bucket, CloudFront distribution, and Route53 record for `beacon.<domain>`
- ACM certificates for both regions
- CloudWatch log group and alarms
- Secrets Manager secrets for backend credentials

## Usage

```bash
cd infra/terraform
terraform init
terraform workspace new staging
terraform plan -var="root_domain_name=example.com"
```

Add the output `nat_gateway_public_ip` to the MongoDB Atlas network allowlist before routing production traffic.
