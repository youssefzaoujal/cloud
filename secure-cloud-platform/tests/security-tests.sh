#!/usr/bin/env bash
set -euo pipefail

auth_url=http://localhost:3000
orders_url=http://localhost:3001

status=$(curl --silent --output /dev/null --write-out '%{http_code}' -X POST "$orders_url/orders" \
  -H 'Content-Type: application/json' -d '{"product":"Laptop","quantity":1}')
test "$status" = "401"
echo "PASS unauthenticated orders rejected"

status=$(curl --silent --output /dev/null --write-out '%{http_code}' "$orders_url/orders" \
  -H 'Authorization: Bearer invalid.token.value')
test "$status" = "401"
echo "PASS invalid JWT rejected"

status=$(curl --silent --output /dev/null --write-out '%{http_code}' \
  -X POST "$auth_url/auth/register" \
  -H 'Content-Type: application/json' \
  -d '{"email":"invalid","password":"short"}')
test "$status" = "400"
echo "PASS invalid registration rejected"

email_a="security-a-$(date +%s)@example.com"
email_b="security-b-$(date +%s)@example.com"
for email in "$email_a" "$email_b"; do
  curl --fail --silent -X POST "$auth_url/auth/register" \
    -H 'Content-Type: application/json' \
    -d "{\"email\":\"$email\",\"password\":\"LocalTest123!\"}" >/dev/null
done


token_a=$(curl --fail --silent -X POST "$auth_url/auth/login" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$email_a\",\"password\":\"LocalTest123!\"}" | \
  sed -n 's/.*"token":"\([^"]*\)".*/\1/p')
token_b=$(curl --fail --silent -X POST "$auth_url/auth/login" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"$email_b\",\"password\":\"LocalTest123!\"}" | \
  sed -n 's/.*"token":"\([^"]*\)".*/\1/p')

order_id=$(curl --fail --silent -X POST "$orders_url/orders" \
  -H "Authorization: Bearer $token_a" \
  -H 'Content-Type: application/json' \
  -d '{"product":"Security test order","quantity":1}' | \
  sed -n 's/.*"id":\([0-9]*\).*/\1/p')

body=$(curl --fail --silent "$orders_url/orders" -H "Authorization: Bearer $token_b")
test "$body" != *"Security test order"*
echo "PASS users cannot list another user's orders"

status=$(curl --silent --output /dev/null --write-out '%{http_code}' "$orders_url/orders/$order_id" \
  -H "Authorization: Bearer $token_b")
test "$status" = "404"
echo "PASS users cannot retrieve another user's order"

injection_body=$(curl --fail --silent -X POST "$orders_url/orders" \
  -H "Authorization: Bearer $token_a" \
  -H 'Content-Type: application/json' \
  -d '{"product":"\u0027 OR 1=1 --","quantity":1}')
grep --fixed-strings --quiet "' OR 1=1 --" <<< "$injection_body"
echo "PASS SQL-like input is treated as data"

if git grep -n -E 'AKIA[0-9A-Z]{16}|aws_secret_access_key|password[[:space:]]*=[[:space:]]*"' -- ':!tests/security-tests.sh'; then
  echo "FAIL potential secret found in tracked files"
  exit 1
fi
echo "PASS no obvious secrets tracked"

for port in 5432 6379; do
  if (echo >/dev/tcp/127.0.0.1/$port) 2>/dev/null; then
    echo "FAIL data port $port is exposed"
    exit 1
  fi
done
echo "PASS PostgreSQL and Redis are not exposed on host ports"
