# Requirements Coverage

This page maps the key AWS services and learning outcomes from the Manara SAA-C03 graduation brief
for Project 6 and Project 8 to concrete repository evidence.

Legend: ✅ implemented as infrastructure code · 📄 designed and documented only · 🧪 verified locally

## Project 6 - ECS Fargate Microservices

### Key AWS Services

| Required service | Status | Evidence |
| --- | --- | --- |
| ECS Fargate | ✅ | `infrastructure/cloudformation/project-06/02-application.yaml`: ECS cluster, three task definitions, three services and autoscaling resources |
| ECR | ✅ | `02-application.yaml`: three repositories with image scanning configuration |
| ALB and target groups | ✅ (HTTP review stack) / 📄 (HTTPS production target) | `02-application.yaml`: load balancer, HTTP listener, three target groups and path-based listener rules; ACM/WAF edge is documented as a target control |
| AWS Cloud Map | ✅ | `02-application.yaml`: private DNS namespace and service discovery resources |
| Secrets Manager | ✅ | `02-application.yaml`: secret resources and task-definition secret references |
| ElastiCache Redis | ✅ | `02-application.yaml`: Redis replication group and subnet group |
| CodePipeline and CodeDeploy | 📄 | `pipeline/README.md` and `architecture/ecs-architecture.py`; the working local equivalent is GitHub Actions |
| X-Ray | 📄 | `architecture/ecs-architecture.py` and `docs/architecture.md` |

### Learning Outcomes

| Outcome | Status | Evidence |
| --- | --- | --- |
| Build container images and define ECS tasks | ✅ 🧪 | `services/*/Dockerfile` and ECS task definitions |
| Separate ECS execution and task roles | ✅ | `security/iam/task-execution-role-policy.json` and service task-role policies |
| Service-to-service discovery | ✅ 🧪 | Cloud Map target resources and Docker Compose service DNS |
| ALB path-based routing | ✅ | Listener rules in `02-application.yaml` |
| Blue/green deployment design | 📄 | `pipeline/README.md` and the rollback alarm documented in the application stack |
| Secure secret handling | ✅ 🧪 | `.env.example`, Secrets Manager references and `tests/security-tests.sh` |

## Project 8 - Security Architecture

### Key AWS Services

| Required service | Status | Evidence |
| --- | --- | --- |
| AWS KMS | ✅ | `infrastructure/cloudformation/project-08/01-foundation.yaml`: three customer-managed keys and aliases |
| Secrets Manager rotation | ✅ | Foundation and application templates document encrypted secret storage and rotation configuration |
| GuardDuty | ✅ | `project-08/02-detection-response.yaml`: GuardDuty detector |
| Security Hub | ✅ | `02-detection-response.yaml`: Security Hub and standards subscriptions |
| AWS Config | ✅ | `02-detection-response.yaml`: Config rules and remediation configuration; see `security/config-auto-remediation.md` |
| CloudTrail | ✅ | `01-foundation.yaml`: multi-region trail, log validation and KMS encryption |
| WAF and Shield Standard | 📄 | `architecture/secure-architecture.py` and `docs/security.md` |
| IAM and SCPs | ✅ | `security/iam/` policy documents, including SCPs and permission boundary |

### Learning Outcomes

| Outcome | Status | Evidence |
| --- | --- | --- |
| Apply KMS CMKs with scoped policies | ✅ | `security/kms-cmk-key-policy.json` and `security/kms-data-key-policy.json` |
| Configure secret rotation design | ✅ | Foundation and application CloudFormation templates |
| Enable GuardDuty and route findings | ✅ | GuardDuty detector and EventBridge severity filtering |
| Aggregate findings in Security Hub | ✅ | Security Hub standards subscriptions |
| Remediate Config drift with SSM | ✅ | Config rules, remediation resources and `security/config-auto-remediation.md` |
| Design least-privilege IAM guardrails | ✅ | `security/iam/` policy documents |

## Deliverables Checklist

| Deliverable | Status |
| --- | --- |
| Solution architecture diagram | ✅ `architecture/solution-architecture.png` plus detailed Project 6 and Project 8 views |
| Public GitHub repository with documentation | ✅ Root README, project README, ADRs and evidence matrix |
| Local application implementation | ✅ Docker Compose, three Node.js services and local tests |
| AWS infrastructure design | ✅ Four CloudFormation stacks validated by `cfn-lint` |
| Live AWS deployment | 📄 Optional and intentionally not included; see `docs/adr/0002-local-implementation-vs-live-deployment.md` |

The repository does not claim live AWS findings, screenshots or deployment output that were not
actually produced. This distinction keeps the assessment evidence reproducible and auditable.
