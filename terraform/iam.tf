resource "aws_iam_role" "iam_role_lambda_generic" {
  name               = "${local.name_prefix}-generic-lambda-role"
  assume_role_policy = "${file("${path.module}/files/lambda-assume-policy.json")}"
}

resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = "${file("${path.module}/files/lambda_logging_policy.json")}"
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = "${aws_iam_role.iam_role_lambda_generic.name}"
  policy_arn = "${aws_iam_policy.lambda_logging.arn}"
}
