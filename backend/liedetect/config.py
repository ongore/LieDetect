import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Settings:
    env: str = os.getenv("FLASK_ENV", "development")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    s3_bucket: Optional[str] = os.getenv("S3_BUCKET_NAME")
    s3_prefix: str = os.getenv("S3_PREFIX", "sessions")
    audio_endpoint: Optional[str] = os.getenv("AUDIO_MODEL_ENDPOINT")
    macro_endpoint: Optional[str] = os.getenv("MACRO_MODEL_ENDPOINT")
    micro_endpoint: Optional[str] = os.getenv("MICRO_MODEL_ENDPOINT")
    whisper_model: str = os.getenv("WHISPER_MODEL", "whisper-1")
    allowed_origins_raw: str = os.getenv("ALLOWED_ORIGINS", "")
    local_media_root: Path = field(default_factory=lambda: Path(os.getenv("LOCAL_MEDIA_ROOT", "storage")))
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "500"))
    use_mock_services: bool = os.getenv("USE_MOCK_SERVICES", "false").lower() == "true"

    @property
    def allowed_origins(self) -> List[str]:
        if not self.allowed_origins_raw:
            return []
        return [origin.strip() for origin in self.allowed_origins_raw.split(",") if origin.strip()]

    def to_flask_config(self) -> Dict[str, object]:
        return {
            "MAX_CONTENT_LENGTH": self.max_upload_mb * 1024 * 1024
        }


settings = Settings()
settings.local_media_root.mkdir(parents=True, exist_ok=True)
