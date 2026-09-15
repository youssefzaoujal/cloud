#!/usr/bin/env bash
set -euo pipefail

for endpoint in \
  http://localhost:3000/health \
  http://localhost:3001/health \
  http://localhost:3002/health; do
  curl --fail --silent "$endpoint" >/dev/null
  echo "PASS $endpoint"
done
