# Security Controls Evidence

This page maps the security claims to concrete repository evidence. AWS services in the target
architecture are documented designs; the local implementation is Docker Compose and does not
pretend to provide AWS-native detection.

| Control | Repository evidence | Local or target |
| --- | --- | --- |
| Network isolation | `docker-compose.yml` backend network uses `internal: true`; CloudFormation creates subnet tiers and security groups | Both |
| Least-privilege IAM | `security/iam/orders-service-task-role-policy.json`, execution role policy and permission boundary | Target |
| Key separation | `security/kms-cmk-key-policy.json` and `security/kms-data-key-policy.json` | Target |
| Secure transport | `security/s3-secure-transport-bucket-policy.json` and TLS/ALB design | Target |
| Audit trail | CloudTrail and encrypted log archive in `project-08/01-foundation.yaml` | Target |
| Threat detection | GuardDuty and Security Hub in `project-08/02-detection-response.yaml` | Target |
| Configuration remediation | `security/config-auto-remediation.md` and Config resources in the detection stack | Target |
| Container hardening | Non-root Dockerfiles, health checks and Trivy CI scan | Local and CI |
| JWT authorization | Auth validation and protected Orders endpoints in `services/` and `tests/security-tests.sh` | Local |
| Secret handling | Local `.env.example`; Secrets Manager references in the ECS target template | Local and target |

## Scope and limitations

No AWS account, live Security Hub score, GuardDuty finding or console screenshot is claimed in this
repository. Those items belong to an optional live-deployment demonstration and must only be added
when they have actually been captured.
