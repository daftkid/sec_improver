resource "aws_cloudwatch_log_group" "key_rotator" {
  name              = "/aws/lambda/${aws_lambda_function.key_func.function_name}"
  retention_in_days = "${var.lambda_log_retention_period}"
}

resource "aws_cloudwatch_log_group" "sg_tuner" {
  name              = "/aws/lambda/${aws_lambda_function.sg_func.function_name}"
  retention_in_days = "${var.lambda_log_retention_period}"
}

resource "aws_cloudwatch_log_group" "res_wiper" {
  name              = "/aws/lambda/${aws_lambda_function.unused_resources_func.function_name}"
  retention_in_days = "${var.lambda_log_retention_period}"
}
