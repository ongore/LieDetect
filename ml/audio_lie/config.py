from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AudioConfig:
    raw_dataset_dir: Path = Path(os.getenv('AUDIO_DATASET_DIR', 'data/raw/ravdess'))
    processed_dir: Path = Path(os.getenv('AUDIO_PROCESSED_DIR', 'data/processed/audio'))
    sample_rate: int = int(os.getenv('AUDIO_SAMPLE_RATE', '22050'))
    n_mfcc: int = int(os.getenv('AUDIO_N_MFCC', '40'))
    frame_length: int = int(os.getenv('AUDIO_FRAME_LENGTH', '2048'))
    hop_length: int = int(os.getenv('AUDIO_HOP_LENGTH', '512'))
    batch_size: int = int(os.getenv('AUDIO_BATCH_SIZE', '32'))
    num_epochs: int = int(os.getenv('AUDIO_NUM_EPOCHS', '30'))
    learning_rate: float = float(os.getenv('AUDIO_LEARNING_RATE', '0.001'))

    def ensure_dirs(self) -> None:
        self.processed_dir.mkdir(parents=True, exist_ok=True)


config = AudioConfig()
config.ensure_dirs()
