# AWS Mapping

| Local component | AWS target |
| --- | --- |
| Docker Compose services | ECS Fargate tasks and services |
| Docker images | Amazon ECR |
| Compose DNS | AWS Cloud Map service discovery |
| PostgreSQL | Amazon RDS for PostgreSQL in private subnets |
| Redis | Amazon ElastiCache for Redis |
| Published API ports | Internal ECS services behind an ALB |
| Environment secrets | AWS Secrets Manager and KMS |
| Container logs | CloudWatch Logs |
| DNS and edge | Route 53, CloudFront, AWS WAF |
| Audit and threat detection | CloudTrail, GuardDuty, Security Hub |

The local stack is the low-cost development implementation. The AWS architecture adds private subnets, security groups, TLS at the load balancer, and managed data services.
