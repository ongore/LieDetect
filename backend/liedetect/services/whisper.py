from __future__ import annotations

import os
from typing import Optional

import requests

from ..config import settings
from ..utils.session_store import MediaRecord, session_store
from .storage import storage_service


class WhisperService:
    def __init__(self) -> None:
        self._api_key = os.getenv('OPENAI_API_KEY')

    def transcribe(self, session_id: str) -> str:
        record = self._select_media(session_id)
        if not record:
            raise ValueError("No media available for transcription")

        # In mock mode (or without an API key), return a fast placeholder without touching the file system.
        if settings.use_mock_services or not self._api_key:
            transcript = f"[mock transcript for {session_id} using {record.role}]"
        else:
            local_path = storage_service.ensure_local_path(record)
            transcript = self._call_whisper(local_path, record)

        session_store.set_transcript(session_id, transcript)
        return transcript

    def _select_media(self, session_id: str) -> Optional[MediaRecord]:
        return session_store.get_media_record(session_id, 'questioner') or session_store.get_media_record(session_id, 'answerer')

    def _call_whisper(self, path, record: MediaRecord) -> str:
        with open(path, 'rb') as media_file:
            response = requests.post(
                'https://api.openai.com/v1/audio/transcriptions',
                headers={'Authorization': f'Bearer {self._api_key}'},
                data={'model': settings.whisper_model},
                files={'file': (path.name, media_file, record.content_type or 'audio/mpeg')}
            )
        response.raise_for_status()
        payload = response.json()
        return payload.get('text', '').strip()


whisper_service = WhisperService()
