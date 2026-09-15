# Local Deployment

```powershell
docker compose up --build -d
docker compose ps
```

Run checks from Git Bash or a Linux CI runner:

```bash
bash tests/health-checks.sh
bash tests/security-tests.sh
bash tests/integration-tests.sh
```

Stop the stack:

```powershell
docker compose down
```

Use `docker compose down -v` only when intentionally deleting local PostgreSQL and Redis data.

Only ports `3000`, `3001`, and `3002` are published. PostgreSQL and Redis remain reachable by service name inside the private backend network.
