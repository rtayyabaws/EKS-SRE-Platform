#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${1:-argocd}"

kubectl get applications.argoproj.io -n "$NAMESPACE" \
  -o custom-columns=NAME:.metadata.name,SYNC:.status.sync.status,HEALTH:.status.health.status