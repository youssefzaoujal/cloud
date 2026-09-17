# Estimated Monthly AWS Cost (Target Architecture)

This is a rough, order-of-magnitude estimate for the target architecture running in `eu-west-1`
at low/development traffic, used to justify **why this project stays local instead of being
deployed live for the review period**. Numbers are approximate list prices, not a quote — always
confirm with the [AWS Pricing Calculator](https://calculator.aws) before any real deployment.

| Component | Sizing assumption | Approx. monthly cost |
|---|---|---|
| ECS Fargate (3 services × 0.25 vCPU / 0.5 GB, always-on) | 3 tasks running 24/7 | ~$28 |
| Application Load Balancer | 1 ALB, low traffic | ~$18 |
| NAT Gateway | 1 NAT Gateway (private subnet egress) | ~$33 + data processing |
| RDS PostgreSQL (Multi-AZ) | db.t4g.micro, Multi-AZ | ~$28 |
| ElastiCache Redis | cache.t4g.micro, single node | ~$12 |
| CloudFront | Low request volume | ~$1–5 |
| Secrets Manager | 3 secrets | ~$1.20 |
| KMS | 1 customer-managed key | ~$1 |
| CloudWatch Logs | Low volume, 30-day retention | ~$2–5 |
| GuardDuty | Account-level, low event volume | ~$3–8 |
| Security Hub | Account-level | ~$1–3 |
| AWS Config | ~5 rules, low resource count | ~$5–10 |
| CloudTrail | 1 trail (management events are free; data events cost extra) | ~$0–2 |
| **Total (development-scale, always-on)** | | **~$135–160/month** |

## Why this matters

Leaving this running for the ~2–4 weeks of graduation project review would cost roughly
**$65–150**, plus the operational risk of managing a live AWS account (credential leakage,
forgetting to tear it down, unexpected data transfer spikes) for zero additional grading value
over a well-documented target architecture with reviewable diagrams-as-code. If the jury requires
live proof, the fastest safe path is a **timeboxed deployment**: `cdk deploy` (or the Terraform
equivalent) the night before the review, record the demo, then `cdk destroy` immediately after —
see `docs/adr/0002-local-implementation-vs-live-deployment.md`.

The biggest cost lever, if this were deployed permanently, would be the NAT Gateway
(~$33/month + per-GB data processing just for egress). A cheaper production alternative worth
mentioning to the jury: replace the NAT Gateway with **VPC Endpoints** (Gateway endpoint for S3,
Interface endpoints for ECR/Secrets Manager/CloudWatch Logs) since none of the three services
need general internet egress — only AWS API access.
