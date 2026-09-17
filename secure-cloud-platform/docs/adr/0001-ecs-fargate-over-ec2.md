# ADR 0001: ECS Fargate over EC2-based ECS or self-managed Kubernetes

**Status:** Accepted

## Context

Project 6 allows any container orchestration approach. The platform has three small,
independently-scaled Node.js services with modest, spiky traffic and no requirement for custom
AMIs, GPU workloads, or host-level customization.

## Decision

Use ECS with the **Fargate** launch type instead of ECS-on-EC2 or self-managed Kubernetes (EKS).

## Alternatives considered

| Option | Rejected because |
|---|---|
| ECS on EC2 | Requires capacity planning, patching, and paying for idle EC2 capacity between scaling events — the opposite of this project's cost-optimization goal |
| Self-managed Kubernetes on EC2 | Operational overhead (control plane, node groups, upgrades) is disproportionate to three small services; no team-scale need for Kubernetes portability |
| Amazon EKS (managed control plane) | Still requires managing worker node capacity (or Fargate profiles, which converges back to this decision) plus a $0.10/hr control plane fee with no benefit over ECS for this workload |

## Consequences

- Positive: no server patching, per-task billing, scales to zero cost when idle (no minimum EC2 fleet)
- Negative: less control over the underlying host (acceptable — the services need no host-level access), and Fargate's per-task pricing is more expensive than EC2 at very high, sustained utilization (not this workload's profile)
