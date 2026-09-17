# Demo Package

This directory is reserved for evidence that is actually produced during a review. No live AWS
deployment evidence is included in the current submission; this is intentional and documented in
[`docs/adr/0002-local-implementation-vs-live-deployment.md`](../docs/adr/0002-local-implementation-vs-live-deployment.md).

## Local demo

1. Start the stack with `docker compose up --build -d`.
2. Show `docker compose ps` with healthy services.
3. Run the health, security and integration checks.
4. Show the committed architecture diagrams and CloudFormation lint result.
5. Stop the stack with `docker compose down -v`.

## Optional AWS demo

A live AWS demonstration is optional and is not claimed by this repository. If performed, add only
real evidence here: a dated video link, deployment output, or screenshots with the AWS region and
resource context visible. Never commit credentials, secret values or fabricated console captures.
