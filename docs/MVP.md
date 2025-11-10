# LieDetect MVP Overview

## Architecture Summary
- **React Native (Expo)** client for capture, upload, and visualization.
- **Flask** backend running on AWS Lambda behind HTTP API Gateway.
- **S3** for media storage, **SageMaker** endpoints for AudioLie, MacroLie, MicroLie models.
- **OpenAI Whisper + LieLLM** for audio transcription and textual emotion weighting.

## Data Flow
1. Mobile client captures video/audio and uploads to /upload.
2. Backend stores media, triggers /liedetect to invoke SageMaker endpoints.
3. Combined emotion vector and micro-expression score persisted in session store.
4. /transcript generates Whisper transcript, obtains LieLLM vector, fuses alignment with micro score to final lie probability.
5. Client fetches enhanced summary and renders percentages, vectors, transcript.

## Key Paths
- Frontend entry: rontend/App.tsx and navigation under rontend/src/navigation.
- Backend factory: ackend/liedetect/__init__.py.
- Model training pipelines: ml/audio_lie, ml/video_lie.
- Infrastructure as code: infra/terraform.
- CI/CD workflow: .github/workflows/deploy.yml.

## Local Setup
`ash
# Frontend
cd frontend
npm install
npx expo start

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --reload
`

Set environment variables via .env.example or Terraform outputs.

## Testing
`ash
cd backend
pytest
`

Frontend linting: 
pm run lint. Model scripts provide their own CLI entry points for training.

## Deployment Checklist
- Train/export AudioLie, MacroLie, MicroLie models and deploy to SageMaker endpoints.
- Package backend as lambda.zip (see ackend/README.md).
- Configure GitHub secrets (AUDIO_ENDPOINT_NAME, MACRO_ENDPOINT_NAME, MICRO_ENDPOINT_NAME, OPENAI_API_KEY).
- Run Terraform apply or let GitHub Actions deploy from main branch.

## Monitoring & Next Steps
- CloudWatch collects Lambda logs (logger namespace liedetect).
- Extend metrics to include inference latency, failure counts.
- Future enhancements: secure auth, multi-user storage, analytics dashboard.
