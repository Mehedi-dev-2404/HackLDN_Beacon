# AWS Deployment Layout

## Frontend

- Upload `apps/web` assets to S3
- Generate environment-specific `runtime-config.js` before upload
- Serve the site through CloudFront
- Point `beacon.<domain>` to CloudFront via Route53

## Backend

- Build the API image from `docker/Dockerfile.api`
- Push to ECR
- Run the API on ECS Fargate behind an ALB
- Point `api.beacon.<domain>` to the ALB via Route53

## Configuration

- Store `MONGO_URI`, `GEMINI_API_KEY`, `ELEVEN_LABS_API_KEY`, and `SERPAPI_KEY` in Secrets Manager
- Set `FRONTEND_BASE_URL` to the public frontend URL
- Set `ALLOWED_ORIGINS` to the frontend hostname only

## Atlas allowlist

- Terraform outputs the NAT Gateway Elastic IP
- Add that public IP to the MongoDB Atlas network allowlist before enabling production traffic

## CI/CD

- API workflow: tests, Docker build, ECR push, ECS deployment
- Web workflow: render `runtime-config.js`, upload to S3, invalidate CloudFront
- Infra workflow: `terraform fmt`, `terraform validate`, `terraform plan`
