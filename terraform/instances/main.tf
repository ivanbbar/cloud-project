#source : https://www.middlewareinventory.com/blog/terraform-create-multiple-ec2-different-config/
#source : https://www.phillipsj.net/posts/generating-ssh-keys-with-terraform/
#source : https://jhooq.com/terraform-generate-ssh-key/
#source : https://github.com/AKSarav/Terraform-Count-ForEach

resource "aws_instance" "aws_instance" {
  for_each = {for server in var.configuration: server.instance_name[0] =>  server}
    
  ami                    =  data.aws_ami.ubuntu2004.id
  instance_type          =  each.value.instance_type
  subnet_id              =  var.subnet_id
  key_name               =  "GroupId-${each.key}"
  tags = {
      Name = "${each.value.instance_name[0]}"
  }
}

resource "aws_key_pair" "generated_key" {

  for_each = {for server in var.configuration: server.instance_name[0] =>  server}
  
  # Name of key: Write the custom name of your key
  key_name   = "GroupId-${each.key}"
  
  # Public Key: The public will be generated using the reference of tls_private_key.ssh
  public_key = tls_private_key.ssh.public_key_openssh
} 

resource "tls_private_key" "ssh" {
  algorithm = "RSA"
  rsa_bits  = "4096"
}

resource "local_file" "private_key" {
  content         = tls_private_key.ssh.private_key_pem
  filename        = "../linode.pem"
}
