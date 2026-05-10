terraform {
  backend "s3" {
    bucket         = "eks-sre-platform-terraform-state"
    key            = "platform/terraform.tfstate"
    region         = "eu-west-2"
    dynamodb_table = "eks-sre-platform-terraform-locks"
    encrypt        = true
  }
}