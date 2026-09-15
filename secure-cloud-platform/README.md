# Secure Cloud-Native Microservices Platform

A local, containerized microservices platform designed to map cleanly to AWS ECS Fargate.

## Quick start

```powershell
docker compose up --build -d
docker compose ps
```

Services:

- Auth API: `http://localhost:3000`
- Orders API: `http://localhost:3001`
- Notifications API: `http://localhost:3002`
- PostgreSQL: internal backend network only
- Redis: internal backend network only

The data services are intentionally not published to the host. Only the API ports are exposed locally.

## Container Security

GitHub Actions scans all three application images with Trivy after the Docker build. The pipeline fails on fixed `HIGH` or `CRITICAL` vulnerabilities. Run the same check locally with `bash tests/container-scan.sh` after installing Trivy.

## AWS Deployment Status

The architecture is designed and mapped for AWS ECS Fargate, ECR, Cloud Map, RDS, ElastiCache, and managed security services. A complete local implementation is provided with Docker Compose for reproducible evaluation. AWS deployment is intentionally not performed to avoid unnecessary cloud costs.

## Verification

```bash
bash tests/health-checks.sh
bash tests/security-tests.sh
bash tests/integration-tests.sh
bash tests/container-scan.sh
```

The container scan requires Trivy locally. GitHub Actions runs the same vulnerability gate automatically after building the images.

## Architecture diagrams

- [Local architecture](architecture/local-architecture.md)
- [AWS target architecture](architecture/aws-architecture.md)
- [Security architecture](architecture/security-architecture.md)

The diagrams are stored as Mermaid source so they remain reviewable in Git and can be rendered or imported into a diagram editor for presentation exports.

## Project structure

```text
services/       Node.js microservices and Dockerfiles
database/       PostgreSQL initialization schema
tests/          Health, security, integration, and container scans
architecture/   Local, AWS, and security diagrams
docs/           Architecture, deployment, security, and AWS mapping
.github/        GitHub Actions CI workflow
```

Register and authenticate before using orders:

```http
POST /auth/register
POST /auth/login
GET /auth/validate
GET /orders
POST /orders
GET /orders/:id
DELETE /orders/:id
GET /notifications
```

See [docs/architecture.md](docs/architecture.md), [docs/security.md](docs/security.md), and [docs/aws-mapping.md](docs/aws-mapping.md) for the design and production mapping.
