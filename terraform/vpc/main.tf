resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "VPC"
  }
}

resource "aws_internet_gateway" "gw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name = "main gw"
  }
}

resource "aws_route_table" "routing_table" {
  vpc_id = aws_vpc.vpc.id

  route = []

  tags = {
    Name = "routing table"
  }
}

resource "aws_route" "r" {
  route_table_id              = aws_route_table.routing_table.id
  destination_ipv6_cidr_block = "::/0"
  egress_only_gateway_id      = aws_internet_gateway.gw.id
}

resource "aws_route_table_association" "a" {
  subnet_id      = var.subnet_id
  route_table_id = aws_route_table.routing_table.id
}