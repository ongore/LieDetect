from __future__ import annotations

from http import HTTPStatus

from flask import Blueprint, jsonify, request, current_app

from ..services.analysis import analysis_service
from ..services.lie_llm import lie_llm_service
from ..services.vector_math import final_lie_score, llm_alignment_score
from ..services.whisper import whisper_service
from ..utils.session_store import session_store

inference_bp = Blueprint('inference', __name__)


@inference_bp.post('/liedetect')
def run_liedetect():
    payload = request.get_json(silent=True) or {}
    session_id = payload.get('sessionId')
    if not session_id:
        return jsonify({'error': 'sessionId is required'}), HTTPStatus.BAD_REQUEST

    try:
        summary = analysis_service.run(session_id)
        current_app.logger.info('liedetect-run', extra={'session_id': session_id})
    except ValueError as exc:
        current_app.logger.warning('liedetect-error', extra={'session_id': session_id, 'error': str(exc)})
        return jsonify({'error': str(exc)}), HTTPStatus.BAD_REQUEST

    response = {'sessionId': session_id, 'summary': summary}
    return jsonify(response)


@inference_bp.post('/transcript')
def transcript():
    payload = request.get_json(silent=True) or {}
    session_id = payload.get('sessionId')
    if not session_id:
        return jsonify({'error': 'sessionId is required'}), HTTPStatus.BAD_REQUEST

    session = session_store.get(session_id)
    if session and session.get('transcript'):
        enriched = _maybe_enrich_summary(session_id, session['transcript'])
        return jsonify({'sessionId': session_id, 'transcript': session['transcript'], 'summary': enriched})

    try:
        transcript_text = whisper_service.transcribe(session_id)
        current_app.logger.info('transcript-generated', extra={'session_id': session_id})
    except Exception as exc:
        # Return a client-friendly error and avoid hanging the request
        current_app.logger.warning('transcript-error', extra={'session_id': session_id, 'error': str(exc)})
        return jsonify({'error': str(exc)}), HTTPStatus.BAD_REQUEST

    enriched_summary = _maybe_enrich_summary(session_id, transcript_text)
    return jsonify({'sessionId': session_id, 'transcript': transcript_text, 'summary': enriched_summary})


def _maybe_enrich_summary(session_id: str, transcript_text: str):
    session = session_store.get(session_id)
    summary = (session or {}).get('summary')
    if not summary:
        return summary

    llm_vector = lie_llm_service.emotion_weights(transcript_text, session_id)
    alignment = llm_alignment_score(summary.get('comparisonVector', []), llm_vector)
    final_score = final_lie_score(summary.get('microScore', 0.0), alignment)

    summary.update({
        'llmVector': llm_vector,
        'alignmentScore': alignment,
        'lieProbability': final_score
    })
    session_store.set_summary(session_id, summary)
    current_app.logger.info('summary-updated', extra={'session_id': session_id, 'alignment': alignment, 'lieProbability': final_score})
    return summary
