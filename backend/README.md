# LieDetect Backend

## Local Development
`ash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app app run --reload
`

The Flask application exposes the following routes:
- POST /upload – store session media in S3/local storage.
- POST /liedetect – orchestrate SageMaker endpoints and persist summary.
- POST /transcript – run Whisper, invoke LieLLM, and update final lie probability.
- GET /session/<id> – fetch session metadata for debugging.

## Packaging for Lambda
`ash
cd backend
pip install -r requirements.txt -t build
cp -r liedetect build/
cp app.py build/
cd build
zip -r ../lambda.zip .
`
Upload lambda.zip when running 	erraform apply or GitHub Actions deployment.

Environment variables are documented in .env.example.
