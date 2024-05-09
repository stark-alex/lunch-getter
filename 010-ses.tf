resource "aws_ses_email_identity" "email_ids" {
  for_each = toset(local.emails)
  email = each.key
}