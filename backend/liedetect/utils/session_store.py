from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from ..config import settings


@dataclass
class MediaRecord:
    session_id: str
    role: str
    key: str
    bucket: Optional[str]
    local_path: Optional[str]
    content_type: str


class SessionStore:
    def __init__(self, meta_root: Path) -> None:
        self.meta_root = meta_root
        self.meta_root.mkdir(parents=True, exist_ok=True)

    def _path(self, session_id: str) -> Path:
        return self.meta_root / f"{session_id}.json"

    def _load(self, session_id: str) -> Dict[str, Any]:
        path = self._path(session_id)
        if not path.exists():
            return {
                "sessionId": session_id,
                "media": {},
                "createdAt": datetime.now(timezone.utc).isoformat()
            }
        return json.loads(path.read_text(encoding="utf-8"))

    def _save(self, session_id: str, payload: Dict[str, Any]) -> None:
        payload["updatedAt"] = datetime.now(timezone.utc).isoformat()
        path = self._path(session_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def update_media(self, session_id: str, role: str, record: MediaRecord) -> None:
        payload = self._load(session_id)
        payload.setdefault("media", {})[role] = {
            "key": record.key,
            "bucket": record.bucket,
            "localPath": record.local_path,
            "contentType": record.content_type
        }
        self._save(session_id, payload)

    def update_media_path(self, record: MediaRecord) -> None:
        payload = self._load(record.session_id)
        media = payload.setdefault("media", {}).setdefault(record.role, {})
        media["localPath"] = record.local_path
        self._save(record.session_id, payload)

    def set_transcript(self, session_id: str, transcript: str) -> None:
        payload = self._load(session_id)
        payload["transcript"] = transcript
        self._save(session_id, payload)

    def set_summary(self, session_id: str, summary: Dict[str, Any]) -> None:
        payload = self._load(session_id)
        payload["summary"] = summary
        self._save(session_id, payload)

    def set_llm_vector(self, session_id: str, vector: Dict[str, float]) -> None:
        payload = self._load(session_id)
        payload["llmVector"] = vector
        self._save(session_id, payload)

    def get(self, session_id: str) -> Optional[Dict[str, Any]]:
        path = self._path(session_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def get_media_record(self, session_id: str, role: str) -> Optional[MediaRecord]:
        payload = self.get(session_id)
        if not payload:
            return None
        entry = payload.get('media', {}).get(role)
        if not entry:
            return None
        return MediaRecord(
            session_id=session_id,
            role=role,
            key=entry.get('key'),
            bucket=entry.get('bucket'),
            local_path=entry.get('localPath'),
            content_type=entry.get('contentType', 'video/mp4')
        )


session_store = SessionStore(settings.local_media_root / "meta")
