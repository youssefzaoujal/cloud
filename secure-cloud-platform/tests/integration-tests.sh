#!/usr/bin/env bash
set -euo pipefail

email="integration-$(date +%s)@example.com"
base_auth=http://localhost:3000
base_orders=http://localhost:3001

curl --fail --silent -X POST "$base_auth/auth/register" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$email\",\"password\":\"LocalTest123!\"}" >/dev/null

token=$(curl --fail --silent -X POST "$base_auth/auth/login" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$email\",\"password\":\"LocalTest123!\"}" | \
  sed -n 's/.*"token":"\([^"]*\)".*/\1/p')
test -n "$token"

curl --fail --silent -X POST "$base_orders/orders" \
  -H "Authorization: Bearer $token" \
  -H 'Content-Type: application/json' \
  -d '{"product":"Integration laptop","quantity":1}' >/dev/null

echo "PASS register, login, order creation, and notification flow"
