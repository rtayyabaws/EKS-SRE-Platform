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


| Terraform | Remote backend bootstrap | Successful | Created S3-backed Terraform state with versioning, encryption and public access blocking |
| Terraform | State locking method | S3 native lockfile | Avoided deprecated DynamoDB state locking and enabled safe remote backend locking |
| Terraform | Platform plan result | 28 to add, 0 to change, 0 to destroy | Validated full EKS platform infrastructure before first apply |
| Terraform | Route53 hosted zone lookup | Successful | Confirmed Terraform can reference existing hosted zone for `nourdemo.com` |


Plan: 28 to add, 0 to change, 0 to destroy. for infra

## EKS Cluster Provisioning

| Metric | Result |
|---|---|
| Terraform resources created | 28 |
| EKS cluster name | eks-sre-platform |
| Kubernetes version | v1.32.13-eks-4136f65 |
| Worker nodes ready | 2/2 |
| Node networking | Private subnets |
| kubectl access | Confirmed |
| IAM access issue resolved | Added EKS access entry + cluster admin policy association |

## GitOps / ArgoCD

| Metric | Result |
|---|---|
| ArgoCD root app | Synced / Healthy |
| cert-manager | Synced / Healthy |
| ClusterIssuer | Synced / Healthy |
| ExternalDNS | Synced / Healthy |
| ingress-nginx | Synced / Healthy |
| Loki | Synced / Healthy |
| Demo app | Synced / Progressing |
| kube-prometheus-stack | Healthy, OutOfSync |

NAME                            READY   STATUS    RESTARTS   AGE
cm-acme-http-solver-2rdwm       1/1     Running   0          64m
sre-demo-app-854688b6f4-tf65x   1/1     Running   0          60s
sre-demo-app-854688b6f4-w89mr   1/1     Running   0          71s
NAMESPACE      NAME                        CLASS    HOSTS              ADDRESS                                                                         PORTS     AGE
sre-demo-app   cm-acme-http-solver-v9dgm   <none>   eks.nourdemo.com   a64e82e543f6b4c44b910975d828d635-04fd99b7fb336104.elb.eu-west-2.amazonaws.com   80        64m
sre-demo-app   sre-demo-app                nginx    eks.nourdemo.com   a64e82e543f6b4c44b910975d828d635-04fd99b7fb336104.elb.eu-west-2.amazonaws.com   80, 443   64m