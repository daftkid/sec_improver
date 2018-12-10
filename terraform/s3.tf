resource "aws_s3_bucket" "report_storage_bucket" {
  bucket = "${local.name_prefix}-report-storage"
  acl    = "private"

  tags {
    Name    = "${local.name_prefix}-report-storage"
    Env     = "${var.env}"
    Product = "${var.product}"
    Contact = "${var.contact}"
  }
}
