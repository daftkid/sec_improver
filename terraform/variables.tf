variable "env" {
  description = "The name of Environment for deployment"
  default     = "development"
}

variable "product" {
  description = "The name of deployed Product"
  default     = "diploma"
}

variable "contact" {
  description = "Email of responsible person"
  default     = "alexandr.mykytenko@gmail.com"
}

variable "runtime" {
  description = "The type of function Runtime"
  default     = "python3.6"
}

variable "lambda_log_retention_period" {
  description = "The number of days for storing logs from Lambda functions"
  default     = 14
}
