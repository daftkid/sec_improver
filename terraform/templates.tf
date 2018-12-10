data "archive_file" "lambda_src" {
  output_path = "lambda_src.zip"
  type        = "zip"
  source_dir  = "${path.module}/templates/src/"
}
