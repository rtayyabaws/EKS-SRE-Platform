# EKS GitOps Platform

A production-style cloud-native platform deployed on Amazon EKS, demonstrating end-to-end infrastructure automation, GitOps delivery, security scanning, and full observability with Prometheus and Grafana.

**Live:** https://eks.nourdemo.com


## Architecture Diagram

![Arch diagram](/docs/screenshots/Architectural diagram.png)

The platform is built across three layers:

- **Infrastructure**: Terraform provisions a multi-AZ VPC, EKS cluster with managed node groups, IAM roles with OIDC federation, ECR, Route53, and ACM certificates. State is managed remotely in S3 with DynamoDB locking.
- **Platform**: ingress-nginx, cert-manager, ExternalDNS, and kube-prometheus-stack are deployed via Helm and managed by Argo CD.
- **Application**: Python/FastAPI service with health, readiness, and Prometheus metrics endpoints, deployed via Argo CD with an HPA for autoscaling.


## Key Components

### Kubernetes & Argo CD

- **Amazon EKS** — managed Kubernetes control plane with node groups running in private subnets
- **Argo CD** — continuously reconciles the cluster against this Git repository; any merged change is reflected in the cluster automatically
- All application manifests (Deployment, Service, Ingress, HPA, ServiceMonitor) are version-controlled and GitOps-managed

### Networking & Ingress

- **ingress-nginx** — the single entry point into the cluster, routing traffic based on Ingress rules
- **AWS Load Balancer** — receives public traffic and forwards to ingress-nginx
- **ExternalDNS** — watches Ingress resources and automatically creates/updates Route53 records; uses IRSA to authenticate to AWS without storing credentials

### Certificate Management

- **cert-manager** — provisions and renews TLS certificates automatically via Let's Encrypt DNS-01 challenge through Route53
- Any Ingress annotated for TLS receives a valid certificate and Kubernetes secret; no manual renewal required

### Observability

- **Prometheus** — scrapes app metrics, kube-state-metrics, node-exporter, kubelet, and ingress-nginx
- **Grafana** — visualises metrics through custom and imported dashboards (JSON exports committed to Git)
- **Loki** — log aggregation for the cluster and application

### Security

- **No long-lived credentials** — GitHub Actions authenticates to AWS via OIDC federation
- **Trivy** — scans every Docker image before it reaches ECR
- **Checkov** — runs against all Terraform and Kubernetes manifests on every pipeline run
- **Private node groups** — EKS workers run in private subnets; only the load balancer is public-facing
- **Least-privilege IAM** — each component (ExternalDNS, cert-manager, GitHub Actions) has its own scoped role

---

## Directory Structure

```
.
├── .github/
│   └── workflows/
│       ├── app-ci.yml                     
│       ├── terraform-apply.yml
│       ├── terraform-destroy.yml
│       └── terraform-plan.yml
│
├── app/                                    
│   ├── Dockerfile
│   ├── main.py                             
│   └── requirements.txt
│
├── argocd/
│   └── apps/                              
│       ├── cert-manager.yaml
│       ├── clusterissuer.yaml
│       ├── external-dns.yaml
│       ├── ingress-nginx.yaml
│       ├── kube-prometheus-stack.yaml
│       ├── loki.yaml
│       ├── root-app.yaml                  
│       └── sre-demo-app.yaml
│
├── dashboards/
│   └── grafana/                          
│       ├── loki-logs.json
│       ├── node-health.json
│       └── sre-app-dashboard.json
│
├── docs/
│   ├── screenshots/                      
│   ├── architecture.md
│   ├── metrics.md
│   └── troubleshooting.md
│
├── helm/
│   └── sre-demo-app/                      
│       ├── templates/
│       ├── Chart.yaml
│       └── values.yaml
│
├── manifests/
│   └── cert-manager/
│       └── clusterissuer.yml
│
├── scripts/
│   ├── check-argocd-sync.sh
│   ├── hpa-test.sh
│   ├── load-test.sh
│   ├── port-forward-grafana.sh
│   └── smoke-test.sh
│
├── terraform/
│   ├── bootstrap/                         
│   ├── modules/
│   │   ├── ecr/
│   │   ├── eks/
│   │   ├── iam/
│   │   ├── route53/
│   │   └── vpc/
│   ├── backend.tf
│   ├── main.tf
│   ├── outputs.tf
│   ├── provider.tf
│   ├── variables.tf
│   ├── versions.tf
│   └── terraform.tfvars.example
│
├── .gitignore
├── .pre-commit-config.yaml                
└── README.md
```

## CI/CD Pipelines

## 4 Pipelines: app-ci.yml, terraform-plan.yml, terraform-apply.yml and terraform-destroy.yml

---

## GitOps Flow

```
git push → GitHub Actions → ECR push → manifest update → Argo CD sync → EKS
```

Argo CD provides drift detection and self-healing. Rollbacks are a `git revert` — no manual cluster intervention required.

![Argo CD](/docs/screenshots/argocd.png)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Cloud | AWS — EKS, VPC, ECR, Route53, ACM, IAM, S3, DynamoDB |
| Infrastructure as Code | Terraform (modular, remote state) |
| GitOps | Argo CD |
| CI/CD | GitHub Actions |
| Ingress | ingress-nginx |
| DNS | ExternalDNS + Route53 |
| TLS | cert-manager + Let's Encrypt |
| Metrics | Prometheus + kube-prometheus-stack |
| Dashboards | Grafana |
| Logs | Loki |
| Autoscaling | Horizontal Pod Autoscaler |
| Security Scanning | Trivy (images), Checkov (IaC) |
| Application | Python / FastAPI |
| Registry | Amazon ECR |

---

## Observability

### Prometheus Targets

Prometheus scrapes:

- Application `/metrics` endpoint via ServiceMonitor
- `kube-state-metrics` — Kubernetes object state
- `node-exporter` — node CPU, memory, disk
- `kubelet` — pod and container metrics
- `ingress-nginx` — request rates and latency

![Prometheus Targets](_screenshots/prometheus-targets.png)

### Grafana Dashboards

Dashboard JSON exports are committed to Git under `/dashboards/` — dashboards are reproducible infrastructure artifacts, not manual configuration.

| Dashboard | Panels |
|---|---|
| SRE Application | HTTP request rate by endpoint, average latency, pod CPU/memory, ready pod count |
| Node Exporter Full | Node resource usage, disk I/O, network throughput |

![SRE Dashboard](/docs/screenshots/grafana%20dash1.png)

---

## Autoscaling

The application has an HPA targeting CPU utilisation. Load testing is used to exercise the scaling behaviour and observe metrics.

```bash
# scripts/load-test.sh
URL="https://eks.nourdemo.com"
while true; do
  curl -s "$URL" > /dev/null
  curl -s "$URL/healthz" > /dev/null
  curl -s "$URL/slow" > /dev/null
  echo "Requests sent at $(date '+%H:%M:%S')"
  sleep 0.2
done
```

> HPA scaling screenshot — _coming soon (metrics-server setup in progress)_

---

## Application Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /` | Root response |
| `GET /healthz` | Liveness probe |
| `GET /readyz` | Readiness probe |
| `GET /slow` | Simulated latency for load testing |
| `GET /metrics` | Prometheus metrics |

---

## Deployment

### Prerequisites

- AWS CLI configured
- Terraform >= 1.5
- `kubectl`, `helm`, `argocd` CLI

### 1. Bootstrap state backend

```bash
cd bootstrap
terraform init && terraform apply
```

### 2. Provision infrastructure

```bash
cp terraform.tfvars.example terraform.tfvars
# fill in your values
terraform init
terraform plan
terraform apply
```

### 3. Configure kubectl

```bash
aws eks update-kubeconfig --region <region> --name <cluster-name>
```

### 4. Install Argo CD and sync platform

```bash
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd -n argocd --create-namespace
kubectl apply -f kubernetes/argocd/
```

Argo CD reconciles all remaining platform components automatically from Git.

---

## Cost Estimate

Approximate monthly cost when running:

| Resource | Cost |
|---|---|
| EKS control plane | ~$73 |
| EC2 worker nodes (2x t3.medium) | ~$60 |
| NAT gateways | ~$32 |
| Load balancer | ~$16 |
| ECR, S3, Route53 | ~$5–10 |
| **Total** | **~$186–191/month** |

> Tear down with `terraform destroy` when not in use to avoid unnecessary costs.

---

## Troubleshooting

> _Coming soon — will cover: Terraform destroy VPC/ENI failures, Prometheus scraping misconfiguration, GitHub Actions S3 403 on state access, and metrics-server setup for HPA._

---

