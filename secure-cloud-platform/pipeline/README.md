# Delivery Pipeline

## Implemented CI

The repository root contains two GitHub Actions workflows:

- `.github/workflows/ci.yml`: installs Node.js dependencies, builds the local containers, scans the images with Trivy, and runs health, security and integration checks.
- `.github/workflows/validate.yml`: lints all four CloudFormation stacks, validates policy JSON and renders the architecture diagrams.

These workflows run without AWS credentials.

## AWS target pipeline

The architecture diagrams and CloudFormation application stack document the intended AWS delivery
path:

```text
GitHub -> CodePipeline -> CodeBuild -> ECR -> CodeDeploy blue/green -> ECS Fargate
```

That AWS CodePipeline is a target design, not a deployed resource. A live implementation would
require a CodeStar connection, ECR repositories, a CodeDeploy ECS deployment group, CloudWatch
rollback alarms and scoped IAM roles.
