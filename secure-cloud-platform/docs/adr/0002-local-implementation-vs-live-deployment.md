# ADR 0002: Local Docker Compose implementation instead of a live AWS deployment

**Status:** Accepted

## Context

The graduation project deliverables require a solution architecture diagram and full
documentation; a live URL or demo video is explicitly listed as **optional but encouraged**. A
full live deployment (ECS Fargate, Multi-AZ RDS, NAT Gateway, WAF, GuardDuty, Security Hub, Config)
costs an estimated $135–160/month if left running (`docs/cost-estimate.md`), and this repository
is being built and reviewed without a funded AWS sandbox.

## Decision

Implement and test the full system locally with Docker Compose, treat the AWS architecture as a
fully specified and documented **target design** (diagrams-as-code, IAM/KMS policy examples,
Config remediation examples), and only perform a live deployment as a timeboxed exercise
immediately before a demo if the jury explicitly requires it — then tear it down the same day.

## What would change for an actual deployment

1. `docker-compose.yml` service definitions → ECS task definitions (1:1 mapping already
   documented in `docs/aws-mapping.md`)
2. Compose environment variables → Secrets Manager secrets referenced by ARN in the task
   definition, decrypted via the CMK in `security/kms-cmk-key-policy.json`
3. Compose internal network → VPC private subnets + security groups (no public route)
4. `docker compose up` → `cdk deploy` / `terraform apply` using the IAM roles in `security/iam/`
5. Manual health checks → CloudWatch alarms wired to SNS (already scaffolded in
   `docs/well-architected-mapping.md`, Reliability pillar)

## Consequences

- Positive: zero idle cloud spend, zero risk of an orphaned AWS resource after the review, all
  architecture claims remain independently verifiable by reading code (diagrams-as-code,
  policy JSON) rather than trusting a screenshot
- Negative: no live URL by default; mitigated by keeping the deployment path fully scripted so a
  timeboxed demo is a same-day exercise, not a multi-day project
