## EKS managed node group AMI unsupported for Kubernetes 1.29

During the first infrastructure apply, the EKS control plane was created successfully, but the managed node group failed with:

`InvalidParameterException: Requested AMI for this version 1.29 is not supported`

Root cause: the configured Kubernetes version was outdated for current EKS managed node group AMI support.

Fix: updated `kubernetes_version` from `1.29` to `1.32` in Terraform variables and re-ran `terraform plan/apply`.


## terraform

Ran into a few validation errors that i forgot to record.