#!/usr/bin/env bash
set -euo pipefail

NAMESPACE="${1:-monitoring}"
SERVICE="${2:-kube-prometheus-stack-grafana}"
LOCAL_PORT="${3:-3000}"
REMOTE_PORT="${4:-80}"

echo "Forwarding Grafana:"
echo "http://localhost:$LOCAL_PORT"

kubectl port-forward -n "$NAMESPACE" "svc/$SERVICE" "$LOCAL_PORT:$REMOTE_PORT"