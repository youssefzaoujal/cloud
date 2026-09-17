# CloudFormation Infrastructure

This directory contains the AWS target infrastructure for the two architecture tracks documented in
this repository. It is reviewable and linted locally; it is not deployed by default.

## Layout

```text
cloudformation/
├── project-06/
│   ├── 01-network.yaml
│   └── 02-application.yaml
└── project-08/
    ├── 01-foundation.yaml
    └── 02-detection-response.yaml
```

## Deployment order

Project 6:

1. `01-network.yaml` creates the VPC, subnet tiers, NAT egress, endpoints and security groups.
2. `02-application.yaml` imports the network exports and creates ECS Fargate, ALB, Cloud Map, RDS,
   ElastiCache, ECR, Secrets Manager and observability resources.

Project 8:

1. `01-foundation.yaml` creates KMS keys, the tamper-evident log archive, CloudTrail and Config.
2. `02-detection-response.yaml` imports the foundation exports and creates GuardDuty, Security Hub,
   Config remediation and EventBridge/Lambda response controls.

## Local validation

From the repository root:

```powershell
python -m pip install cfn-lint
cfn-lint secure-cloud-platform/infrastructure/cloudformation/project-06/*.yaml secure-cloud-platform/infrastructure/cloudformation/project-08/*.yaml
```

The same command runs in `.github/workflows/validate.yml` on every push and pull request.

## Deployment status

These templates are an AWS target design. The repository intentionally does not deploy them to a
live account, so no AWS credentials or account-specific values are committed. Review parameters,
exports, IAM permissions, quotas and regional service availability before a time-boxed deployment.
