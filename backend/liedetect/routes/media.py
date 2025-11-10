from __future__ import annotations

from http import HTTPStatus

from flask import Blueprint, jsonify, request, current_app

from ..services.storage import storage_service
from ..utils.session_store import session_store

media_bp = Blueprint('media', __name__)


@media_bp.post('/upload')
def upload_media():
    session_id = request.form.get('sessionId')
    role = (request.form.get('role') or 'answerer').lower()
    file = request.files.get('video')

    if not session_id or not file:
        return jsonify({'error': 'sessionId and video file are required'}), HTTPStatus.BAD_REQUEST

    try:
        record = storage_service.save_media(session_id, role, file)
        current_app.logger.info('media-upload', extra={'session_id': session_id, 'role': role, 'key': record.key})
    except ValueError as exc:
        return jsonify({'error': str(exc)}), HTTPStatus.BAD_REQUEST

    response = {
        'sessionId': session_id,
        'role': role,
        'videoKey': record.key,
        'bucket': record.bucket,
        'contentType': record.content_type
    }
    return jsonify(response), HTTPStatus.CREATED


@media_bp.get('/session/<session_id>')
def get_session(session_id: str):
    payload = session_store.get(session_id)
    if not payload:
        current_app.logger.warning('session-miss', extra={'session_id': session_id})
        return jsonify({'error': 'Session not found'}), HTTPStatus.NOT_FOUND
    return jsonify(payload)
