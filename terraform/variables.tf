variable "aws_access_key" {
  type        = string
  description = "visible in Terraform Cloud"
}

variable "aws_secret_key" {
  type        = string
  description = "sensitive in Terraform Cloud"
}

variable "aws_region" {
  default     = "us-east-1"
}

variable "users" {
  description = "Name"
  type = list(object({
        name = string
    }))
}

variable "configuration" {
  description = "configuration"
  type = list(object({
        instance_name = list(string),
        instance_type = string  
    }))
}

variable "sgs"{
    description = "Each security groups data"
    type = list(object({
        name = string,
        description = string,
        ingress = list(object({
            from_port = number,
            to_port = number,
            protocol = string,
            cidr_blocks = list(string)
        })),
        egress = list(object({
            from_port = number,
            to_port = number,
            protocol = string,
            cidr_blocks = list(string)
        }))

    }))
}

variable "association"{
    type = list(object({
        name = string,
        instance_id = string,
        security_group_id = string
    }))
}