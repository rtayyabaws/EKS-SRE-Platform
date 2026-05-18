# Troubleshooting — Development Notes

## EKS managed node group AMI unsupported for Kubernetes 1.29

**Problem:** EKS control plane created successfully but managed node group failed with `InvalidParameterException: Requested AMI for this version 1.29 is not supported`.

**Cause:** Kubernetes version 1.29 was outdated for current EKS managed node group AMI support.

**Fix:** Updated `kubernetes_version` from `1.29` to `1.32` in `terraform/terraform.tfvars.example` and re-ran `terraform apply`.

---

## kubectl authentication failed after EKS provisioning

**Problem:** After provisioning the EKS cluster, `kubectl get nodes` returned `error: You must be logged in to the server`.

**Cause:** EKS requires the IAM principal to be explicitly granted cluster access. The local IAM user `nour-nonroot` had AWS permissions but was not mapped to Kubernetes cluster access.

**Fix:** Added an EKS access entry in Terraform and associated the `AmazonEKSClusterAdminPolicy` managed policy to the IAM user.

```hcl
resource "aws_eks_access_entry" "cluster_admin" {
  cluster_name  = var.cluster_name
  principal_arn = "arn:aws:iam::595552412690:user/nour-nonroot"
  type          = "STANDARD"
}

resource "aws_eks_access_policy_association" "cluster_admin" {
  cluster_name  = var.cluster_name
  principal_arn = "arn:aws:iam::595552412690:user/nour-nonroot"
  policy_arn    = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"
  access_scope { type = "cluster" }
}
```

---

## EKS orphaned ENIs blocking subnet deletion

**Problem:** `terraform destroy` fails with `DependencyViolation` on public subnets and IGW after node group terminates.

**Cause:** EKS attaches ENIs to subnets for pod networking. These are not always released immediately after the node group is destroyed, leaving dependencies that block subnet and IGW deletion.

**Fix:** Added a retry-based ENI cleanup step to the destroy pipeline that runs after the NLB wait — finds all available ENIs in the VPC and deletes them before Terraform attempts to delete the subnets.