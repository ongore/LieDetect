from __future__ import annotations

from typing import Dict, List

from ..config import settings
from ..utils.session_store import session_store
from .sage_maker import sagemaker_gateway
from .vector_math import average_vectors, fuse_lie_scores


class AnalysisService:
    def run(self, session_id: str) -> Dict[str, object]:
        session = session_store.get(session_id)
        if not session:
            raise ValueError(f"Unknown session: {session_id}")

        media = session.get('media', {})
        media_record = media.get('answerer') or media.get('questioner')
        if not media_record:
            raise ValueError("Session has no uploaded media")

        payload = {
            'sessionId': session_id,
            'videoKey': media_record.get('key'),
            'bucket': media_record.get('bucket'),
            'role': 'answerer' if media.get('answerer') else 'questioner'
        }

        audio_result = self._invoke_endpoint(settings.audio_endpoint, payload)
        macro_result = self._invoke_endpoint(settings.macro_endpoint, payload)
        micro_result = self._invoke_endpoint(settings.micro_endpoint, payload)

        audio_vector = audio_result.get('emotion_vector', []) or [0.0] * 8
        macro_vector = macro_result.get('emotion_vector', []) or [0.0] * 8
        combined_vector = average_vectors([audio_vector, macro_vector])

        lie_probability = fuse_lie_scores(
            audio_result.get('lie_score', 0.0),
            macro_result.get('lie_score', 0.0),
            micro_result.get('lie_score', 0.0)
        )

        summary = {
            'lieProbability': lie_probability,
            'audioScore': audio_result.get('lie_score', 0.0),
            'macroScore': macro_result.get('lie_score', 0.0),
            'microScore': micro_result.get('lie_score', 0.0),
            'comparisonVector': combined_vector,
            'audioVector': audio_vector,
            'macroVector': macro_vector
        }
        session_store.set_summary(session_id, summary)
        return summary

    def _invoke_endpoint(self, endpoint_name: str | None, payload: Dict[str, object]) -> Dict[str, object]:
        if not endpoint_name:
            return {'lie_score': 0.0, 'emotion_vector': []}
        return sagemaker_gateway.invoke(endpoint_name, payload)


analysis_service = AnalysisService()
