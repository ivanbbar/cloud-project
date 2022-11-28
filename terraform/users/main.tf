resource "aws_iam_user" "users" {
  for_each = {for user in var.users: user.name => user}
  name = each.value.name
}

resource "aws_iam_access_key" "accesskey" {
  for_each = {for user in var.users: user.name => user}
  user = aws_iam_user.users[each.value.name].name
}

resource "local_file" "private_user_key" {
  for_each        = {for key in aws_iam_access_key.accesskey: key.user => key}
  content         = each.value.ses_smtp_password_v4
  filename        = "../${each.value.user}--user_key.pem"
}

