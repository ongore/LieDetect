from __future__ import annotations

import json
import random
from typing import Any, Dict

import boto3

from ..config import settings


class SageMakerGateway:
    def __init__(self) -> None:
        self._runtime = None
        if not settings.use_mock_services:
            self._runtime = boto3.client('sagemaker-runtime', region_name=settings.aws_region)

    def _mock_response(self, endpoint: str) -> Dict[str, Any]:
        random.seed(endpoint)
        emotion_vector = [round(random.random(), 3) for _ in range(7)]
        lie_score = round(sum(emotion_vector) / len(emotion_vector), 3)
        return {
            "emotion_vector": emotion_vector,
            "lie_score": lie_score
        }

    def invoke(self, endpoint_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if not endpoint_name:
            raise ValueError("Endpoint name is required")

        if not self._runtime:
            return self._mock_response(endpoint_name)

        response = self._runtime.invoke_endpoint(
            EndpointName=endpoint_name,
            ContentType='application/json',
            Body=json.dumps(payload).encode('utf-8')
        )
        body = response.get('Body')
        if not body:
            raise RuntimeError("Empty response from SageMaker endpoint")
        data = json.loads(body.read().decode('utf-8'))
        return data


sagemaker_gateway = SageMakerGateway()
