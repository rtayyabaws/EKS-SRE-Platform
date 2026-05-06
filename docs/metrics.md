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