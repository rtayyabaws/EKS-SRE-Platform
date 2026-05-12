terraform {
  backend "s3" {
    bucket       = "eks-sre-platform-terraform-state"
    key          = "platform/terraform.tfstate"
    region       = "eu-west-2"
    encrypt      = true
    use_lockfile = true
  }
}