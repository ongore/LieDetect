resource "aws_lambda_function" "liedetect" {
  function_name = "${var.project_name}-api"
  role          = aws_iam_role.lambda_role.arn
  handler       = "wsgi_handler.handler"
  runtime       = "python3.11"
  filename      = var.lambda_artifact_path
  timeout       = 60
  memory_size   = 1024

  environment {
    variables = {
      FLASK_ENV            = "production"
      AWS_REGION           = var.aws_region
      S3_BUCKET_NAME       = aws_s3_bucket.media.bucket
      AUDIO_MODEL_ENDPOINT = var.audio_endpoint_name
      MACRO_MODEL_ENDPOINT = var.macro_endpoint_name
      MICRO_MODEL_ENDPOINT = var.micro_endpoint_name
      OPENAI_API_KEY       = var.openai_api_key
    }
  }
}

resource "aws_apigatewayv2_api" "http" {
  name          = "${var.project_name}-http"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id                 = aws_apigatewayv2_api.http.id
  integration_type       = "AWS_PROXY"
  integration_uri        = aws_lambda_function.liedetect.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "proxy" {
  api_id    = aws_apigatewayv2_api.http.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "prod" {
  api_id      = aws_apigatewayv2_api.http.id
  name        = "prod"
  auto_deploy = true
}

resource "aws_lambda_permission" "allow_apigw" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.liedetect.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.http.execution_arn}/*/*"
}
