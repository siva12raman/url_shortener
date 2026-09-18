output "function_url" {
  description = "Public HTTPS Function URL for the URL Shortener API"
  value       = aws_lambda_function_url.app_url.function_url
}

output "ecr_repository_url" {
  description = "Amazon ECR Repository URL"
  value       = aws_ecr_repository.app.repository_url
}

output "lambda_function_name" {
  description = "AWS Lambda Function Name"
  value       = aws_lambda_function.app.function_name
}
