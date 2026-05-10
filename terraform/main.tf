module "vpc" {
  source = "./modules/vpc"

  project_name         = var.project_name
  vpc_cidr             = var.vpc_cidr
  availability_zones   = var.availability_zones
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  tags                 = var.tags
}

module "iam" {
  source = "./modules/iam"

  project_name = var.project_name
  tags         = var.tags
}

module "eks" {
  source = "./modules/eks"

  cluster_name       = var.cluster_name
  kubernetes_version = var.kubernetes_version

  cluster_role_arn = module.iam.eks_cluster_role_arn
  node_role_arn    = module.iam.eks_node_role_arn

  private_subnet_ids = module.vpc.private_subnet_ids

  instance_types    = var.instance_types
  node_desired_size = var.node_desired_size
  node_min_size     = var.node_min_size
  node_max_size     = var.node_max_size

  tags = var.tags
}

module "ecr" {
  source = "./modules/ecr"

  repository_name = var.repository_name
  max_image_count = var.max_image_count
  tags            = var.tags
}

module "route53" {
  source = "./modules/route53"

  domain_name = var.domain_name
}