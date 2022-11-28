terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  access_key = "${var.aws_access_key}"
  secret_key = "${var.aws_secret_key}"
  region     = "${var.aws_region}"
}
module "instances"{
  source = "./instances"
  subnet_id = module.subnet.subnet_id
  configuration = var.configuration
}

module "vpc"{
  source = "./vpc"
  subnet_id = module.subnet.subnet_id
}

module "security_group"{
  source = "./security_group"
  sgs = var.sgs
  association = var.association
  vpc_id = module.vpc.vpc_id
}

module "subnet"{
  source = "./subnet"
  vpc_id = module.vpc.vpc_id
  av_subnet_zone = "us-east-1a"
}

module "users"{
  source = "./users"
  users = var.users
}


