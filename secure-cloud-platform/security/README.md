# Security Policy Examples

These files are reviewable examples for the AWS target architecture. They are not deployed
credentials and must not be applied without replacing the placeholders and reviewing the scope.

## Placeholders

- `ACCOUNT_ID`: the AWS account ID.
- `PLATFORM_CMK_ID`: the customer-managed KMS key ID.
- Region names and resource names: adapt to the deployment environment.

The local project is intentionally not deployed to AWS. The policies document the least-privilege
intent and the controls that would be implemented in a time-boxed target deployment.

## Files

- `kms-cmk-key-policy.json`: separates KMS key administration from key usage.
- `iam/task-execution-role-policy.json`: permits the ECS agent to pull the Orders image, read its secret and write logs.
- `iam/orders-service-task-role-policy.json`: permits the Orders application to publish events, emit scoped metrics and send X-Ray data.
- `iam/scp-deny-root-and-region.json`: example organization guardrails for root usage, approved regions and GuardDuty protection.
- `config-auto-remediation.md`: AWS Config detection paired with SSM corrective automation.

Review all principals, resource ARNs, conditions and service-linked-role requirements before use.
