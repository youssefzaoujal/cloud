# AWS Well-Architected Framework Mapping

This project is evaluated against all six pillars, not just Security, to show the fusion of
Project 6 (Containers) and Project 8 (Security) was a deliberate architectural decision rather
than a checklist exercise.

## 1. Operational Excellence

| Practice | Evidence |
|---|---|
| Infrastructure as reproducible code | `docker-compose.yml` + `architecture/solution-architecture.py` (diagram-as-code) |
| CI/CD with automated gates | `.github/workflows/ci.yml`: build → npm dependency audit → health/security/integration tests; `validate.yml` runs CloudFormation, policy and diagram validation |
| Health checks on every service | `docker-compose.yml` healthcheck blocks; AWS target uses ALB target group health checks + ECS service auto-replacement |
| Documented rollback | Blue/green via CodeDeploy in the ECS target (see `docs/aws-mapping.md`) |

## 2. Security

| Practice | Evidence |
|---|---|
| Least-privilege IAM | `security/iam/orders-service-task-role-policy.json` — scoped to 3 actions, no wildcards |
| Encryption at rest | `security/kms-cmk-key-policy.json` — customer-managed key for Secrets Manager, RDS, ElastiCache |
| Encryption in transit | TLS terminated at ALB; JWT over HTTPS between client and services |
| Detective controls | GuardDuty findings feed Security Hub (`architecture/security-architecture.mmd`) |
| Corrective controls | `security/config-auto-remediation.md` — Config rule + SSM Automation auto-fixes drift |
| Network isolation | Postgres/Redis on an `internal: true` Docker network, no host port published — same pattern as an AWS private subnet with no route to an Internet Gateway |
| No bastion / no long-lived SSH keys | Systems Manager Session Manager only (`docs/deployment.md`) |

## 3. Reliability

| Practice | Evidence |
|---|---|
| Multi-AZ target | RDS Multi-AZ and ECS services spread across 2+ AZs in the target architecture |
| Graceful degradation | `orders-service` depends on Redis for caching only — a Redis outage degrades latency, not availability (verify in `tests/integration-tests.sh`) |
| Automated recovery | ECS service scheduler replaces unhealthy tasks; `restart: unless-stopped` locally |

## 4. Performance Efficiency

| Practice | Evidence |
|---|---|
| Caching | Redis caches each user's order list for 30s (`docs/architecture.md`) |
| Right-sized compute | Fargate task-level CPU/memory sizing per service instead of one shared EC2 fleet |
| Edge caching | CloudFront in front of ALB in the target architecture |

## 5. Cost Optimization

| Practice | Evidence |
|---|---|
| No idle cloud spend during development | Local Docker Compose implementation instead of a live 24/7 AWS deployment — see `docs/adr/0002-local-implementation-vs-live-deployment.md` |
| Serverless-adjacent compute | Fargate avoids paying for idle EC2 capacity |
| Estimated cost documented before any deployment decision | `docs/cost-estimate.md` |

## 6. Sustainability

| Practice | Evidence |
|---|---|
| On-demand only, no over-provisioned always-on infrastructure | Same Fargate + no idle deployment rationale as above |
| Regional choice minimizing data transfer | Single-region target (`eu-west-1`) instead of unnecessary multi-region replication, since this platform has no DR requirement (contrast with Project 5) |
