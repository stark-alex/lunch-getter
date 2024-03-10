resource "aws_cloudwatch_event_rule" "every_sunday" {
  name        = "every-sunday"
  description = "Trigger Lambda Every Sunday evening"

  schedule_expression = "cron(0 18 ? * SUN *)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.every_sunday.name
  target_id = "SendToLambda"
  arn       = module.lambda_function.lambda_function_arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = module.lambda_function.lambda_function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_sunday.arn
}