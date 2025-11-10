variable "project_name" {
  type        = string
  description = "Base name for LieDetect resources"
  default     = "liedetect"
}

variable "aws_region" {
  type        = string
  description = "AWS region for deployment"
  default     = "us-east-1"
}

variable "lambda_artifact_path" {
  type        = string
  description = "Path to the zipped Flask backend artifact"
}

variable "audio_endpoint_name" {
  type        = string
  description = "SageMaker endpoint name for AudioLie"
}

variable "macro_endpoint_name" {
  type        = string
  description = "SageMaker endpoint name for MacroLie"
}

variable "micro_endpoint_name" {
  type        = string
  description = "SageMaker endpoint name for MicroLie"
}

variable "openai_api_key" {
  type        = string
  description = "OpenAI API key for Whisper/LieLLM"
  sensitive   = true
}
