variable "aws_region" {
  type        = string
  description = "AWS Region for deployment"
  default     = "us-east-1"
}

variable "app_name" {
  type        = string
  description = "Application and resource name prefix"
  default     = "url-shortener"
}

variable "lambda_memory_size" {
  type        = number
  description = "Memory allocated to Lambda function in MB (128 MB for cost optimization)"
  default     = 128
}

variable "lambda_architecture" {
  type        = string
  description = "Instruction set architecture (arm64 for Apple Silicon Mac builds & cost optimization)"
  default     = "arm64"
}
