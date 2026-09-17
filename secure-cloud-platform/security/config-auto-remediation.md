# AWS Config Rule + Automatic Remediation (Project 8 requirement)

This documents the auto-remediation control referenced in `docs/security.md`: detect and fix
non-compliant resources without human intervention, using an AWS Config managed rule plus an
SSM Automation document.

## Rule: `s3-bucket-server-side-encryption-enabled`

Detects any S3 bucket in the account (e.g. a future bucket added for static asset hosting or
Athena/data-lake extensions) that does not have default encryption enabled.

```json
{
  "ConfigRuleName": "secure-platform-s3-encryption-enabled",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED"
  },
  "Scope": {
    "ComplianceResourceTypes": ["AWS::S3::Bucket"]
  }
}
```

## Remediation: SSM Automation document

When the rule reports `NON_COMPLIANT`, an SSM Automation document runs automatically and
applies default SSE-KMS encryption using the platform CMK, then re-triggers evaluation.

```json
{
  "ConfigRuleName": "secure-platform-s3-encryption-enabled",
  "TargetId": "AWS-EnableS3BucketEncryption",
  "Parameters": {
    "AutomationAssumeRole": {
      "StaticValue": {
        "Values": ["arn:aws:iam::ACCOUNT_ID:role/secure-platform-config-remediation-role"]
      }
    },
    "BucketName": {
      "ResourceValue": { "Value": "RESOURCE_ID" }
    },
    "SSEAlgorithm": {
      "StaticValue": { "Values": ["aws:kms"] }
    },
    "KMSMasterKeyID": {
      "StaticValue": { "Values": ["PLATFORM_CMK_ID"] }
    }
  },
  "Automatic": true,
  "MaximumAutomaticAttempts": 3,
  "RetryAttemptSeconds": 60
}
```

## Why this matters for the exam mapping

This is the concrete implementation of the "Design secure architectures" and "Automate
compliance" line items in `docs/architecture.md` — a Config rule alone only *detects* drift; the
SSM Automation association is what makes it self-healing, which is exactly the distinction the
SAA-C03 Security domain tests (detective control vs. corrective control).

## Second example: restrict SSH ingress

The same pattern applies to `restricted-ssh` (flags any security group allowing `0.0.0.0/0` on
port 22) paired with the `AWS-DisablePublicAccessForSecurityGroup` remediation action — relevant
here because this platform has no bastion host at all (Systems Manager Session Manager is the
only access path, see `docs/deployment.md`), so any open SSH rule found by Config is by
definition a misconfiguration to auto-close, not a legitimate access path.
