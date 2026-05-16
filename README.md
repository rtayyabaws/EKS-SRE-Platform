# EKS SRE Platform

A production-style cloud-native platform deployed on Amazon EKS, demonstrating end-to-end infrastructure automation, GitOps delivery, security scanning, and full observability with Prometheus and Grafana.

**Live:** https://eks.nourdemo.com



## Architecture

![Architecture Diagram](/docs/screenshots/Architectural%20diagram.png)

The platform is built across three layers:

- **Infrastructure** — Terraform provisions a multi-AZ VPC, EKS cluster with managed node groups, IAM roles with OIDC federation, ECR, Route53, and ACM certificates. State is managed remotely in S3 with native S3 locking.
- **Platform** — ingress-nginx, cert-manager, ExternalDNS, and kube-prometheus-stack are deployed via Helm and managed by Argo CD.
- **Application** — Python/FastAPI service with health, readiness, and Prometheus metrics endpoints, deployed via Argo CD with an HPA for autoscaling.



## Key Components

### Kubernetes & Argo CD

- **Amazon EKS** — managed Kubernetes control plane with node groups running in private subnets
- **Argo CD** — continuously reconciles the cluster against this Git repository; any merged change is reflected in the cluster automatically
- All application manifests (Deployment, Service, Ingress, HPA, ServiceMonitor) are version-controlled and GitOps-managed

![Argo CD — all apps synced and healthy](/docs/screenshots/argocd.png)

### Networking & Ingress

- **ingress-nginx** — the single entry point into the cluster, routing traffic based on Ingress rules
- **AWS Load Balancer** — receives public traffic and forwards to ingress-nginx
- **ExternalDNS** — watches Ingress resources and automatically creates/updates Route53 records; uses EKS Pod Identity to authenticate to AWS without storing credentials

### Certificate Management

- **cert-manager** — provisions and renews TLS certificates automatically via Let's Encrypt DNS-01 challenge through Route53
- Any Ingress annotated for TLS receives a valid certificate and Kubernetes secret; no manual renewal required

### Observability

- **Prometheus** — scrapes app metrics, kube-state-metrics, node-exporter, kubelet, and ingress-nginx via ServiceMonitors
- **Grafana** — visualises metrics through custom and imported dashboards; JSON exports committed to Git as reproducible infrastructure artifacts
- **Loki** — deployed via Argo CD for log aggregation, with Promtail shipping logs from all pods across both nodes

### Autoscaling

- **Horizontal Pod Autoscaler** — scales the FastAPI app between 2 and 6 replicas based on CPU utilisation
- **metrics-server** — deployed via Argo CD, provides the Kubernetes Metrics API that feeds real-time CPU data to the HPA

### Security

- **No long-lived credentials** — GitHub Actions authenticates to AWS via OIDC federation; no static keys stored in secrets
- **Trivy** — scans every Docker image for vulnerabilities before it reaches ECR
- **Checkov** — runs against all Terraform manifests on every pipeline run; failures are documented and suppressed with explicit reasoning in `.checkov.yaml`
- **Private node groups** — EKS workers run in private subnets; only the load balancer is public-facing
- **Least-privilege IAM** — each workload component (ExternalDNS, cert-manager) has its own scoped IAM role via Pod Identity

---

## Tech Stack

| Layer | Technology |
|---|---|
| Cloud | AWS — EKS, VPC, ECR, Route53, ACM, IAM, S3 |
| Infrastructure as Code | Terraform (modular, remote state) |
| GitOps | Argo CD |
| CI/CD | GitHub Actions |
| Ingress | ingress-nginx |
| DNS | ExternalDNS + Route53 |
| TLS | cert-manager + Let's Encrypt |
| Metrics | Prometheus + kube-prometheus-stack |
| Dashboards | Grafana |
| Logs | Loki + Promtail |
| Autoscaling | Horizontal Pod Autoscaler + metrics-server |
| Security Scanning | Trivy (images), Checkov (IaC) |
| Application | Python / FastAPI |
| Registry | Amazon ECR |

---

## Directory Structure

```
.
├── .github/
│   └── workflows/
│       ├── app-ci.yml                     # Docker build, Trivy scan, ECR push
│       ├── terraform-apply.yml
│       ├── terraform-destroy.yml
│       └── terraform-plan.yml
│
├── app/                                   # FastAPI application
│   ├── Dockerfile
│   ├── main.py                            # /, /healthz, /readyz, /slow, /metrics
│   └── requirements.txt
│
├── argocd/
│   └── apps/                             # Argo CD Application manifests
│       ├── cert-manager.yaml
│       ├── clusterissuer.yaml
│       ├── external-dns.yaml
│       ├── ingress-nginx.yaml
│       ├── kube-prometheus-stack.yaml
│       ├── loki.yaml
│       ├── metrics-server.yaml
│       ├── root-app.yaml                 # App of apps entry point
│       └── sre-demo-app.yaml
│
├── dashboards/
│   └── grafana/                          # Dashboard JSON exports — version controlled
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
│   └── sre-demo-app/                     # Helm chart for FastAPI app
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
│   ├── bootstrap/                        # One-time S3 state backend setup
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
├── .checkov.yaml                         # Checkov skip rules with documented reasoning
├── .gitignore
├── .pre-commit-config.yaml               # Pre-commit hooks — terraform fmt, validate
└── README.md
```

---

## CI/CD Pipelines

### Pipeline 1 — App CI (`app-ci.yml`)

Triggered on push to `main` for changes under `app/` or `helm/`:

1. Docker image build
2. Trivy vulnerability scan
3. Push to ECR (tagged with Git SHA)
4. Update Helm values with new image tag
5. Commit back to Git with `[skip ci]` — Argo CD detects the change and syncs

![App CI Pipeline](/docs/screenshots/app%20ci.png)

### Pipeline 2 — Terraform Plan (`terraform-plan.yml`)

Triggered on pull requests touching `terraform/`:

1. `terraform fmt` and `terraform validate`
2. Checkov IaC security scan
3. `terraform plan` — shows exactly what will change

![Terraform Plan Pipeline](/docs/screenshots/terraform%20plan.png)

### Pipeline 3 — Terraform Apply (`terraform-apply.yml`)

Manual trigger only — provisions or updates AWS infrastructure:

1. `terraform apply -auto-approve`
2. Bootstraps ArgoCD via Helm
3. Applies root app — ArgoCD takes over and syncs the full platform

![Terraform Apply Pipeline](/docs/screenshots/tf%20apply%20pipeline.png)

### Pipeline 4 — Terraform Destroy (`terraform-destroy.yml`)

Manual trigger only — tears down infrastructure cleanly:

1. Deletes ingress-nginx service to release the AWS NLB before VPC deletion
2. `terraform destroy` scoped to exclude the OIDC provider and GitHub Actions role

![Terraform Destroy Pipeline](/docs/screenshots/terraform%20destroy.png)

---

## GitOps Flow

```
git push → GitHub Actions → ECR push → manifest update → Argo CD sync → EKS
```

Argo CD provides drift detection and self-healing. Rollbacks are a `git revert` — no manual cluster intervention required. The app of apps pattern (`root-app.yaml`) means a single manifest bootstraps the entire platform.

---

## Observability

### Grafana — SRE Application Dashboard

Custom dashboard tracking HTTP request rate by endpoint, average request latency, pod CPU and memory usage, and ready pod count. Dashboard JSON is committed to Git — reproducible as an infrastructure artifact.

![Grafana SRE Dashboard](/docs/screenshots/grafana%20dash1.png)

### Prometheus Targets

Prometheus scrapes:

- Application `/metrics` endpoint via ServiceMonitor
- `kube-state-metrics` — Kubernetes object state
- `node-exporter` — node CPU, memory, disk
- `kubelet` — pod and container metrics
- `ingress-nginx` — request rates and latency

![Prometheus Targets](/docs/screenshots/Prometheus.png)

---

## Autoscaling

The FastAPI app is configured with an HPA targeting 60% CPU utilisation, scaling between 2 and 6 replicas. The `/slow` endpoint performs CPU-intensive computation to drive CPU above the threshold, making it purpose-built for triggering and demonstrating autoscaling behaviour under load.

Load test (`scripts/load-test.sh`) sends 20 concurrent requests per second across all endpoints. Under sustained load the HPA scales from 2 replicas to 6 within minutes, then scales back down once traffic stops — demonstrating the full scale-out and scale-in cycle.

![HPA Scaling Demo](/docs/screenshots/hpa%20demo%20test%202%20.png)

---

## Application Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /` | Root response |
| `GET /healthz` | Liveness probe |
| `GET /readyz` | Readiness probe |
| `GET /slow` | CPU-intensive endpoint for load testing and HPA demonstration |
| `GET /metrics` | Prometheus metrics |

---

## Deployment

### Prerequisites

- AWS CLI configured
- Terraform >= 1.5
- `kubectl`, `helm`, `argocd` CLI

### 1. Bootstrap state backend

```bash
cd terraform/bootstrap
terraform init && terraform apply
```

### 2. Provision infrastructure and bootstrap platform

```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
# fill in your values
cd terraform
terraform init
terraform apply
```

The apply pipeline also handles ArgoCD installation and platform bootstrap automatically. To run manually after apply:

```bash
aws eks update-kubeconfig --region eu-west-2 --name eks-sre-platform
helm repo add argo https://argoproj.github.io/argo-helm
helm upgrade --install argocd argo/argo-cd -n argocd --create-namespace --wait
kubectl apply -f argocd/apps/root-app.yaml
```

Argo CD reconciles all platform components from Git automatically.

### 3. Tear down

```bash
# Via pipeline (recommended) — handles NLB cleanup automatically
# Trigger terraform-destroy.yml from GitHub Actions

# Or locally
kubectl delete svc ingress-nginx-controller -n ingress-nginx
sleep 90
cd terraform && terraform destroy \
  -target=module.eks \
  -target=module.vpc \
  -target=module.ecr \
  -target=aws_eks_pod_identity_association.external_dns
```

> The OIDC provider and GitHub Actions IAM role are excluded from destroy to preserve CI/CD pipeline functionality on next apply.

---

## Cost Estimate

Approximate monthly cost when running:

| Resource | Cost |
|---|---|
| EKS control plane | ~$73 |
| EC2 worker nodes (2× t3.medium) | ~$60 |
| NAT gateways (2×) | ~$32 |
| Load balancer | ~$16 |
| ECR, S3, Route53 | ~$5–10 |
| **Total** | **~$186–191/month** |

> Tear down with the destroy pipeline when not in use.

---

## Troubleshooting

### Terraform destroy hangs on VPC deletion

**Problem:** `terraform destroy` pends indefinitely when deleting the VPC.

**Cause:** ingress-nginx creates an AWS Network Load Balancer outside of Terraform's state. AWS refuses to delete the VPC while the NLB is still attached.

**Fix:** Delete the ingress-nginx controller service first to release the NLB, wait 90 seconds for AWS to deprovision it, then run destroy. The destroy pipeline handles this automatically.

---

### GitHub Actions S3 403 on state access

**Problem:** Terraform plan/apply pipeline fails with `AccessDenied` on S3 `HeadObject`.

**Cause:** The GitHub Actions IAM role was missing S3 permissions for the Terraform state bucket.

**Fix:** Added `s3:GetObject`, `s3:PutObject`, `s3:DeleteObject`, `s3:ListBucket` to the GitHub Actions role policy in `modules/iam/main.tf`.

---

### Stale Terraform state lock

**Problem:** `Error acquiring the state lock` when running Terraform locally after a cancelled pipeline.

**Cause:** Cancelling a GitHub Actions pipeline mid-run leaves the S3 lock file (`terraform.tfstate.tflock`) in place.

**Fix:** Delete the lock file directly from S3:

```bash
aws s3api delete-object \
  --bucket eks-sre-platform-terraform-state \
  --key platform/terraform.tfstate.tflock \
  --region eu-west-2
```

---

### OIDC provider destroyed breaking CI/CD

**Problem:** GitHub Actions pipeline fails with `No OpenIDConnect provider found` after a full `terraform destroy`.

**Cause:** The OIDC provider was destroyed along with the rest of the infrastructure, removing the trust relationship that allows GitHub Actions to authenticate to AWS.

**Fix:** Added `lifecycle { prevent_destroy = true }` to the OIDC provider and GitHub Actions IAM role. The destroy pipeline uses `-target` to exclude these resources. If ever accidentally destroyed, recreate manually:

```bash
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

---

### HPA showing `<unknown>` targets

**Problem:** `kubectl get hpa` shows `cpu: <unknown>/60%` and pods never scale.

**Cause:** metrics-server was not deployed, so the Kubernetes Metrics API was unavailable and HPA had no CPU data source.

**Fix:** Added metrics-server as an Argo CD managed application (`argocd/apps/metrics-server.yaml`). Once deployed, `kubectl top pods` returns real data and HPA scales correctly.

---

## Key Learnings

- GitOps with Argo CD means Git is the only interface for deployments — no manual `kubectl apply`, no configuration drift, rollbacks are a `git revert`
- Committing Grafana dashboard JSON to Git treats observability as infrastructure, not manual ops configuration
- OIDC federation eliminates the operational risk of long-lived AWS credentials in CI/CD — the GitHub Actions role assumes permissions per-job with no stored secrets
- HPA requires both a manifest and a metrics source — the HPA spec alone does nothing without metrics-server providing the Kubernetes Metrics API
- `time.sleep()` in a FastAPI endpoint does not generate CPU load — HPA measures CPU utilisation, not request latency; CPU-intensive computation is required to trigger scaling
- Real operational issues (state locks, NLB blocking VPC deletion, OIDC provider lifecycle) surface the kind of judgment that doesn't come from tutorial projects