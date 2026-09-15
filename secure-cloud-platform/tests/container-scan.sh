#!/usr/bin/env bash
set -euo pipefail

if ! command -v trivy >/dev/null 2>&1; then
  echo "Trivy is required for container scanning: https://trivy.dev/latest/getting-started/installation/"
  exit 1
fi

for image in \
  secure-cloud-platform-auth-service:latest \
  secure-cloud-platform-orders-service:latest \
  secure-cloud-platform-notifications-service:latest; do
  trivy image --ignore-unfixed --severity HIGH,CRITICAL --exit-code 1 "$image"
done