resource "aws_lambda_function" "key_func" {
  function_name = "${local.name_prefix}-key-rotator"
  handler       = "key_scanner.lambda_handler"
  role          = "${aws_iam_role.iam_role_lambda_generic.arn}"
  runtime       = "${var.runtime}"

  filename         = "${data.archive_file.lambda_src.output_path}"
  source_code_hash = "${data.archive_file.lambda_src.output_base64sha256}"
}

resource "aws_lambda_function" "sg_func" {
  function_name = "${local.name_prefix}-sg-tuner"
  handler       = "sg_scanner.lambda_handler"
  role          = "${aws_iam_role.iam_role_lambda_generic.arn}"
  runtime       = "${var.runtime}"

  filename         = "${data.archive_file.lambda_src.output_path}"
  source_code_hash = "${data.archive_file.lambda_src.output_base64sha256}"
}

resource "aws_lambda_function" "unused_resources_func" {
  function_name = "${local.name_prefix}-wiper"
  handler       = "res_wiper.lambda_handler"
  role          = "${aws_iam_role.iam_role_lambda_generic.arn}"
  runtime       = "${var.runtime}"

  filename         = "${data.archive_file.lambda_src.output_path}"
  source_code_hash = "${data.archive_file.lambda_src.output_base64sha256}"
}
