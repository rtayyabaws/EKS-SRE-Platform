# Metrics & Improvements

This document tracks measurable engineering improvements, operational metrics, and optimisation decisions made throughout the project lifecycle.

The goal is to quantify technical impact for:
- CV achievements
- interview discussions
- architecture decisions
- operational improvements
- production-readiness evidence

---

## Metrics To Track

| Category | Metric | Before | After | Impact |
|---|---|---|---|---|
| Docker | Image size |  |  | Faster pulls / reduced attack surface |
| CI/CD | Commit → deployment time |  |  | Faster delivery |
| Infrastructure | Terraform provisioning time |  |  | Reproducible infrastructure |
| Kubernetes | Pod recovery/self-healing time |  |  | Improved resilience |
| Autoscaling | HPA scale-up time |  |  | Better workload handling |
| Security | Trivy vulnerabilities |  |  | Reduced security exposure |
| Security | Checkov findings resolved |  |  | Hardened infrastructure |
| GitOps | ArgoCD sync time |  |  | Faster reconciliation |
| Performance | Average response latency |  |  | Improved responsiveness |
| Observability | Dashboards / telemetry sources |  |  | Increased visibility |
| Automation | Manual deployment steps |  |  | Reduced operational overhead |
| Cost | Infrastructure optimisation changes |  |  | Reduced AWS spend |

---

## Evidence Collection

For each improvement:
- capture screenshots
- save pipeline logs
- record timings
- document reasoning
- explain operational/business impact

Example:
- Grafana dashboard screenshots
- ArgoCD sync evidence
- Trivy scan outputs
- Terraform apply timings
- Load test results

1st metric tracked 22:03, 06/05/2026,  
# docker images sre-demo-app:local                                   ░▒▓ 

IMAGE                ID             DISK USAGE   CONTENT SIZE   EXTRA
sre-demo-app:local   b092aaf8b889        244MB         58.5MB    U 

## Helm Metrics

| Category | Metric | Result | Operational Impact |
|---|---|---|---|
| Helm | Helm chart lint validation | 0 failures | Verified chart structure and syntax before deployment |
| Helm | Helm lint execution time | 0.709s | Fast validation cycle improves deployment feedback loop |
| Helm | Rendered Kubernetes resources | 8 resources | Deployment, Service, Ingress, HPA, PDB, ServiceMonitor, NetworkPolicy and ServiceAccount successfully templated |
| Kubernetes | Health probes implemented | Liveness + Readiness | Enables Kubernetes self-healing and safe traffic routing |
| Kubernetes | Horizontal Pod Autoscaler | Enabled | Supports automatic workload scaling under CPU pressure |
| Kubernetes | PodDisruptionBudget | Enabled | Maintains service availability during node maintenance or disruption |
| Observability | Prometheus metrics endpoint | `/metrics` exposed | Enables application-level monitoring and scraping |
| Security | NetworkPolicy enforcement | Enabled | Restricts inbound pod traffic and improves workload isolation |
| Availability | Replica count | 2 replicas | Improves workload resilience and reduces single-pod failure impact |