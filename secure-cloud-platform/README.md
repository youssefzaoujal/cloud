# AWS Solutions Architect - Associate | Secure Cloud-Native Microservices

**Author:** Youssef Zaoujal  
**Program:** Manara - AWS Solutions Architect Associate (SAA-C03)  
**Repository:** https://github.com/youssefzaoujal/cloud

This repository contains a reproducible containerized microservices platform designed as an AWS Solutions Architect - Associate graduation project. The local implementation runs with Docker Compose and maps to a target AWS architecture based on ECS Fargate.

## Table of Contents

- [Solution Overview](#solution-overview)
- [Quick Start](#quick-start)
- [AWS Mapping](#aws-mapping)
- [Project Status](#project-status)
- [Container Security](#container-security)
- [CloudFormation Infrastructure](#cloudformation-infrastructure)
- [Architecture Diagrams](#architecture-diagrams)
- [How to Reproduce the Diagrams](#how-to-reproduce-the-diagrams)
- [SAA-C03 Coverage](#saa-c03-coverage)
- [Verification](#verification)
- [Project Structure](#project-structure)

## Solution Overview

The application is split into three independently deployable Node.js services:

| Service | Responsibility | Local data dependency |
| --- | --- | --- |
| Auth | Registration, login and JWT validation | PostgreSQL |
| Orders | Order creation, retrieval and deletion | PostgreSQL and Redis |
| Notifications | Notification API and order-event handling | PostgreSQL |

The local stack keeps PostgreSQL and Redis on an internal Docker network. Only the three API services expose host ports.

## Quick Start

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

## AWS Mapping

| Local component | AWS target |
| --- | --- |
| Docker Compose services | ECS Fargate services |
| Docker images | Amazon ECR |
| Compose DNS | AWS Cloud Map |
| PostgreSQL | Amazon RDS for PostgreSQL |
| Redis | Amazon ElastiCache for Redis |
| Environment secrets | AWS Secrets Manager and KMS |
| Container logs | Amazon CloudWatch Logs |
| Edge and DNS | Application Load Balancer, CloudFront, WAF and Route 53 |

AWS deployment is intentionally not performed in this repository to avoid unnecessary cloud costs. The AWS diagram is a documented target architecture, not evidence of deployed resources.

## Project Status

The local application is implemented and tested with Docker Compose. The AWS target is represented
by diagrams-as-code, four CloudFormation stacks, and separate IAM, KMS, SCP, S3 and Config policy
examples. The live deployment is intentionally excluded because it is an optional deliverable and
would create ongoing AWS costs.

## Container Security

GitHub Actions scans all three application images with Trivy after the Docker build. The pipeline fails on fixed `HIGH` or `CRITICAL` vulnerabilities. Run the same check locally with `bash tests/container-scan.sh` after installing Trivy.

## Verification

```bash
bash tests/health-checks.sh
bash tests/security-tests.sh
bash tests/integration-tests.sh
bash tests/container-scan.sh
```

The container scan requires Trivy locally. GitHub Actions runs the same vulnerability gate automatically after building the images.

## CloudFormation Infrastructure

The AWS target templates are documented in [infrastructure/README.md](infrastructure/README.md).
They are split into network/application stacks for Project 6 and foundation/detection-response
stacks for Project 8. `cfn-lint` validates all four templates in the root GitHub Actions workflow.

## Architecture Diagrams

- [Local architecture](architecture/local-architecture.md)
- [AWS target architecture](architecture/aws-architecture.md)
- [Security architecture](architecture/security-architecture.md)
- [AWS target diagram source](architecture/solution-architecture.py)
- [AWS target diagram image](architecture/solution-architecture.png)

The diagrams are stored as Mermaid and Python source so they remain reviewable, reproducible and suitable for presentation exports.

## How to Reproduce the Diagrams

Install the Python package and Graphviz once:

```powershell
python -m pip install diagrams
winget install --id Graphviz.Graphviz --exact
```

From the repository root, regenerate the AWS diagram with:

```powershell
$env:Path = "C:\Program Files\Graphviz\bin;" + $env:Path
python architecture/solution-architecture.py
```

The script writes `architecture/solution-architecture.png` next to the source file.

## SAA-C03 Coverage

| Exam domain | Evidence in this project |
| --- | --- |
| Design secure architectures | Internal backend network, JWT validation, container scanning and secrets mapping |
| Design resilient architectures | Health checks, service isolation and restart policies |
| Design high-performing architectures | Independent services, Redis and the ECS Fargate target mapping |
| Design cost-optimized architectures | Local Docker Compose implementation and no unnecessary AWS deployment |

## Project Structure

```text
services/       Node.js microservices and Dockerfiles
database/       PostgreSQL initialization schema
tests/          Health, security, integration, and container scans
architecture/   Local, AWS, and security diagrams
infrastructure/ CloudFormation target stacks and validation notes
security/       IAM, KMS, SCP, S3 and Config policy examples
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
