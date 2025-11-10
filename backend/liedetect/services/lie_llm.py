from __future__ import annotations

import json
import os
from typing import Dict

import requests

from ..config import settings
from ..utils.session_store import session_store


class LieLLMService:
    def __init__(self) -> None:
        self._api_key = os.getenv('OPENAI_API_KEY')
        self._model = os.getenv('LIE_LLM_MODEL', 'gpt-4o-mini')

    def emotion_weights(self, transcript: str, session_id: str) -> Dict[str, float]:
        if settings.use_mock_services or not self._api_key:
            weights = self._mock_weights()
        else:
            weights = self._invoke_openai(transcript)
        session_store.set_llm_vector(session_id, weights)
        return weights

    def _invoke_openai(self, transcript: str) -> Dict[str, float]:
        prompt = (
            "You analyze transcripts for deceptive cues. Return a JSON object with emotion weights "
            "for angry, calm, disgust, fearful, happy, neutral, sad, surprised between 0 and 1."
        )
        payload = {
            'model': self._model,
            'messages': [
                {'role': 'system', 'content': prompt},
                {'role': 'user', 'content': transcript}
            ],
            'response_format': {'type': 'json_object'}
        }
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {self._api_key}', 'Content-Type': 'application/json'},
            data=json.dumps(payload)
        )
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']
        parsed = json.loads(content)
        return {emotion: float(value) for emotion, value in parsed.items()}

    def _mock_weights(self) -> Dict[str, float]:
        return {
            'angry': 0.1,
            'calm': 0.2,
            'disgust': 0.1,
            'fearful': 0.1,
            'happy': 0.2,
            'neutral': 0.2,
            'sad': 0.05,
            'surprised': 0.05
        }


lie_llm_service = LieLLMService()
