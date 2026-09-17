# Optional Demo Checklist

The live AWS URL, recorded video and console screenshots are optional deliverables. They are not
included in this repository because no live AWS deployment was performed; see
[`docs/adr/0002-local-implementation-vs-live-deployment.md`](adr/0002-local-implementation-vs-live-deployment.md).
The local evidence path is reproducible without AWS credentials:

- [ ] **90-second screen recording** of `docker compose up --build -d` → `docker compose ps`
      showing all 5 containers healthy → `curl` calls to register, login, create an order,
      list orders (cache hit on the second call) → notification created as a side effect
- [ ] **Screenshot of the Trivy scan output** in a GitHub Actions run, showing 0 CRITICAL/HIGH
      vulnerabilities — this is your strongest single piece of evidence for the Security domain
- [ ] **Screenshot of `tests/security-tests.sh` passing** (rejected request without JWT, rejected
      SQL-injection-style payload, etc.)
- [x] **Regenerate the architecture PNGs** with the three scripts under `architecture/`; the
      outputs are committed and checked by GitHub Actions.
- [ ] Add the repo **description and topics** on GitHub (Settings → General): e.g. "aws",
      "saa-c03", "ecs-fargate", "microservices", "security" — a repo with zero topics reads as
      unfinished before the jury even opens a file

The optional AWS evidence must only be added after it has actually been captured. Do not commit
credentials, secret values, fabricated screenshots or an unverified Security Hub score.
