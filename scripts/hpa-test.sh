#!/bin/bash

echo "Watching HPA and app pods in sre-demo-app namespace..."
echo "Press CTRL+C to stop."

watch -n 2 '
echo "=== HPA ==="
kubectl get hpa -n sre-demo-app
echo ""
echo "=== Pods ==="
kubectl get pods -n sre-demo-app
'