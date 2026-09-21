output "ecr_repository_url" {
  description = "ECR repository URL"
  value       = aws_ecr_repository.app.repository_url
}

output "ecr_repository_name" {
  description = "ECR repository name"
  value       = aws_ecr_repository.app.name
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.app.function_name
}

output "function_url" {
  description = "Public Lambda Function URL"
  value       = aws_lambda_function_url.app.function_url
}

output "image_uri" {
  description = "Deployed container image URI"
  value       = local.image_uri
}
