from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class VideoConfig:
    raw_dataset_dir: Path = Path(os.getenv('VIDEO_DATASET_DIR', 'data/raw/video'))
    processed_dir: Path = Path(os.getenv('VIDEO_PROCESSED_DIR', 'data/processed/video'))
    frame_rate: int = int(os.getenv('VIDEO_FRAME_RATE', '1'))
    image_size: int = int(os.getenv('VIDEO_IMAGE_SIZE', '224'))
    batch_size: int = int(os.getenv('VIDEO_BATCH_SIZE', '32'))
    num_epochs: int = int(os.getenv('VIDEO_NUM_EPOCHS', '40'))
    learning_rate: float = float(os.getenv('VIDEO_LEARNING_RATE', '0.0005'))

    def ensure_dirs(self) -> None:
        self.processed_dir.mkdir(parents=True, exist_ok=True)


config = VideoConfig()
config.ensure_dirs()
