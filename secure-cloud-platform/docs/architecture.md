# Architecture

The local platform runs three Node.js services with Docker Compose:

- `auth-service` exposes registration, login, and JWT validation on port 3000.
- `orders-service` exposes authenticated order CRUD on port 3001.
- `notifications-service` stores order notifications on port 3002.
- PostgreSQL stores users, orders, and notifications.
- Redis caches each user's order list for 30 seconds.

The APIs are attached to a `frontend` network and a private `backend` network. PostgreSQL and Redis are attached only to `backend`, which is marked `internal`; neither data service publishes a host port.

Service-to-service traffic uses Compose DNS names, never container IP addresses. Orders calls `http://notifications-service:3002` when an order is created.

The API containers run as the non-root `node` user and expose health endpoints for orchestration.
