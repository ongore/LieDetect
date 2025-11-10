# Infrastructure Deployment

Terraform templates under infra/terraform provision the AWS resources required for LieDetect:

- S3 buckets for session uploads and model artifacts.
- Lambda function hosting the Flask backend (deployed as a zipped artifact).
- HTTP API Gateway wired to the Lambda function.
- IAM permissions to invoke SageMaker endpoints for AudioLie, MacroLie, and MicroLie.

## Prerequisites
- Terraform >= 1.3
- AWS credentials with permissions for IAM, S3, Lambda, API Gateway, and SageMaker invocation.
- Zipped Lambda artifact (build the Flask backend and package dependencies).

## Usage
`
cd infra/terraform
terraform init
terraform apply \
  -var "lambda_artifact_path=../dist/lambda.zip" \
  -var "audio_endpoint_name=audio-lie-endpoint" \
  -var "macro_endpoint_name=macro-lie-endpoint" \
  -var "micro_endpoint_name=micro-lie-endpoint" \
  -var "openai_api_key="
`

Outputs include the API Gateway invoke URL and the session media bucket name. Update the React Native app's EXPO_PUBLIC_API_URL to point to the invoke URL.
