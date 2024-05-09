resource "aws_iam_policy" "ses_send" {
  name        = "ses-send-${terraform.workspace}"
  description = "ses-send-${terraform.workspace}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "ses:SendEmail",
          "ses:SendRawEmail"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

resource "aws_iam_policy" "secrets_read" {
  name        = "secret-read-${terraform.workspace}"
  description = "secret-read-${terraform.workspace}"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "secretsmanager:GetResourcePolicy",
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret",
          "secretsmanager:ListSecretVersionIds"
        ],
        "Resource": [
          "arn:aws:secretsmanager:us-east-2:339712893998:secret:lunch-getter-config-u3XiEG"
        ]
      },
      {
        "Effect": "Allow",
        "Action": "secretsmanager:ListSecrets",
        "Resource": "*"
      }
    ]
  })
}

module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "lunch-getter-${terraform.workspace}"
  description   = "Lunch Getter Lambda (${terraform.workspace})"
  handler       = "lunch_getter.handler"
  runtime       = "python3.12"
  timeout = 60

  source_path = "./src"

  environment_variables = {
    SCHOOL_ID  = "b4435b07-cb6d-4fc3-972b-7bf2d4deea6a"
    PERSON_ID  = "ca3665a5-f84c-433e-8a10-f9148ebf9230"
    EMAILS     = join(",", local.emails)
  }

  attach_policies    = true
  policies           = [
    aws_iam_policy.ses_send.arn,
    aws_iam_policy.secrets_read.arn
  ]
  number_of_policies = 2
}