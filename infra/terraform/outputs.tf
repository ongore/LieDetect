output "api_url" {
  description = "Invoke URL for API Gateway"
  value       = aws_apigatewayv2_stage.prod.invoke_url
}

output "media_bucket" {
  value       = aws_s3_bucket.media.bucket
  description = "S3 bucket storing session videos"
}
