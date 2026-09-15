# Security

- Passwords are hashed with bcrypt before storage.
- Login returns a short-lived JWT; order routes require `Authorization: Bearer <token>`.
- Helmet, CORS, JSON body limits, and rate limiting are enabled on every API.
- SQL queries use PostgreSQL parameters instead of string interpolation.
- Runtime secrets are supplied through environment variables and `.env` is ignored.
- Containers run as the unprivileged `node` user.
- GitHub Actions scans application images with Trivy and fails on fixed high or critical vulnerabilities.

For AWS, map JWT/database values to Secrets Manager, encryption to KMS, network controls to security groups, and audit logs to CloudTrail and CloudWatch.
