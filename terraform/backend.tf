terraform {
  backend "s3" {
    bucket       = "205930609978-rehan-eks-sre-tfstate"
    key          = "platform/terraform.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
