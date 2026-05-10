#!/usr/bin/env bash
set -euo pipefail

APP_URL="${1:-https://eks.nourdemo.com}"

echo "Running smoke tests against: $APP_URL"

curl -fsS "$APP_URL/healthz"
echo " healthz OK"

curl -fsS "$APP_URL/readyz"
echo " readyz OK"

curl -fsS "$APP_URL/version"
echo " version OK"

curl -fsS "$APP_URL/metrics" > /dev/null
echo " metrics OK"

echo "Smoke tests passed"