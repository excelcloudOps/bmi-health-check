variable "aws_region" {
  type        = string
  description = "AWS region for all resources"
  default     = "us-east-2"
}

variable "project_name" {
  type        = string
  description = "Name prefix for resources"
  default     = "bmi-health-check"
}

variable "image_tag" {
  type        = string
  description = "ECR image tag to deploy to Lambda"
  default     = "latest"
}

variable "lambda_memory_mb" {
  type        = number
  description = "Lambda memory size in MB"
  default     = 512
}

variable "lambda_timeout_seconds" {
  type        = number
  description = "Lambda timeout in seconds"
  default     = 10
}
