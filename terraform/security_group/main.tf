resource "aws_security_group" "allow_tls" {
  for_each    = {for sg in var.sgs: sg.name => sg}

  name        = each.value.name
  vpc_id      = var.vpc_id

  ingress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/16"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  tags = {
    Name = each.value.name
  }
}

resource "aws_network_interface_sg_attachment" "sg_attachment" {
  for_each = {for assoc in var.association: assoc.name => assoc}
  security_group_id    = each.value.security_group_id
  network_interface_id = each.value.instance_id
}