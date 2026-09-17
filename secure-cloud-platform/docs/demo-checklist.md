# Optional Demo Checklist (high ROI, low effort)

The instructions mark a live URL / recorded video as optional but encouraged. Full AWS deployment
isn't required to produce convincing evidence — these all run locally in under 10 minutes and are
worth far more to a jury than the text alone:

- [ ] **90-second screen recording** of `docker compose up --build -d` → `docker compose ps`
      showing all 5 containers healthy → `curl` calls to register, login, create an order,
      list orders (cache hit on the second call) → notification created as a side effect
- [ ] **Screenshot of the Trivy scan output** in a GitHub Actions run, showing 0 CRITICAL/HIGH
      vulnerabilities — this is your strongest single piece of evidence for the Security domain
- [ ] **Screenshot of `tests/security-tests.sh` passing** (rejected request without JWT, rejected
      SQL-injection-style payload, etc.)
- [ ] **Regenerate `solution-architecture.png`** right before submission (`python
      architecture/solution-architecture.py`) so it's committed as an actual image, not just
      referenced — GitHub renders `.mmd` Mermaid files but a jury skimming the repo should see the
      diagram inline in the README without clicking through
- [ ] Add the repo **description and topics** on GitHub (Settings → General): e.g. "aws",
      "saa-c03", "ecs-fargate", "microservices", "security" — a repo with zero topics reads as
      unfinished before the jury even opens a file

None of this requires an AWS account or any spend.
