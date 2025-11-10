from __future__ import annotations

from pathlib import Path
from typing import Optional

import boto3
from werkzeug.datastructures import FileStorage

from ..config import settings
from ..utils.session_store import MediaRecord, session_store


class StorageService:
    def __init__(self) -> None:
        self._s3_client = None
        if settings.s3_bucket and not settings.use_mock_services:
            self._s3_client = boto3.client('s3', region_name=settings.aws_region)

    @property
    def s3_enabled(self) -> bool:
        return self._s3_client is not None and settings.s3_bucket is not None

    def save_media(self, session_id: str, role: str, file: FileStorage) -> MediaRecord:
        if not session_id:
            raise ValueError("session_id is required")
        if role not in {"questioner", "answerer"}:
            raise ValueError("role must be 'questioner' or 'answerer'")

        key = f"{settings.s3_prefix}/{session_id}/{role}.mp4"
        content_type = file.mimetype or 'video/mp4'
        local_path: Optional[Path] = None

        if self.s3_enabled:
            file.stream.seek(0)
            self._s3_client.upload_fileobj(
                Fileobj=file.stream,
                Bucket=settings.s3_bucket,  # type: ignore[arg-type]
                Key=key,
                ExtraArgs={'ContentType': content_type}
            )
        else:
            local_path = settings.local_media_root / key
            local_path.parent.mkdir(parents=True, exist_ok=True)
            file.save(local_path)

        record = MediaRecord(
            session_id=session_id,
            role=role,
            key=key,
            bucket=settings.s3_bucket,
            local_path=str(local_path) if local_path else None,
            content_type=content_type
        )
        session_store.update_media(session_id, role, record)
        return record

    def ensure_local_path(self, record: MediaRecord) -> Path:
        if record.local_path:
            path = Path(record.local_path)
            if path.exists():
                return path
        if not self.s3_enabled:
            raise FileNotFoundError("Local media file is unavailable")
        if not record.bucket or not record.key:
            raise FileNotFoundError("Media record missing bucket/key")

        download_path = settings.local_media_root / record.key
        download_path.parent.mkdir(parents=True, exist_ok=True)
        self._s3_client.download_file(record.bucket, record.key, str(download_path))  # type: ignore[arg-type]
        record.local_path = str(download_path)
        session_store.update_media_path(record)
        return download_path


storage_service = StorageService()
