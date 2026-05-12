## EKS managed node group AMI unsupported for Kubernetes 1.29

During the first infrastructure apply, the EKS control plane was created successfully, but the managed node group failed with:

`InvalidParameterException: Requested AMI for this version 1.29 is not supported`

Root cause: the configured Kubernetes version was outdated for current EKS managed node group AMI support.

Fix: updated `kubernetes_version` from `1.29` to `1.32` in Terraform variables and re-ran `terraform plan/apply`.


## terraform

Ran into a few validation errors that i forgot to record.





## kubectl authentication failed after EKS provisioning

### Issue

After successfully provisioning the EKS cluster with Terraform, `kubectl` could not authenticate to the Kubernetes API server.

Command:

```bash
aws eks update-kubeconfig \
  --region eu-west-2 \
  --name eks-sre-platform

kubectl get nodes

error: You must be logged in to the server (the server has asked for the client to provide credentials)

Cause

The EKS cluster was successfully created, but the IAM principal used locally was not mapped to Kubernetes cluster access.

Although the AWS IAM user had permissions to interact with AWS services, EKS requires the IAM principal to be explicitly granted cluster access.

The active IAM identity was:

arn:aws:iam::595552412690:user/nour-nonroot
Fix

Added an EKS access entry and associated the AWS managed cluster admin policy using Terraform.