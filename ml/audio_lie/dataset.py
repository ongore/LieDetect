from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple

import torch
from torch.utils.data import Dataset

from .config import config
from .constants import BAD_EMOTIONS, EMOTION_CODE_MAP, EMOTION_INDEX
from .features import extract_and_pad


@dataclass
class AudioSample:
    path: Path
    emotion: str
    intensity: str
    statement: str
    repetition: str
    actor: int
    modality: str
    vocal_channel: str

    @property
    def lie_label(self) -> float:
        return 1.0 if self.emotion in BAD_EMOTIONS else 0.0


def parse_filename(path: Path) -> AudioSample:
    parts = path.stem.split('-')
    if len(parts) != 7:
        raise ValueError(f"Unexpected filename: {path.name}")
    modality, vocal, emotion_code, intensity, statement, repetition, actor = parts
    emotion = EMOTION_CODE_MAP.get(emotion_code)
    if not emotion:
        raise ValueError(f"Unknown emotion code {emotion_code} in {path.name}")
    return AudioSample(
        path=path,
        emotion=emotion,
        intensity='strong' if intensity == '02' else 'normal',
        statement='dogs' if statement == '02' else 'kids',
        repetition=repetition,
        actor=int(actor),
        modality=modality,
        vocal_channel=vocal
    )


def load_dataset(directory: Path) -> List[AudioSample]:
    if not directory.exists():
        raise FileNotFoundError(f"Dataset directory not found: {directory}")
    samples: List[AudioSample] = [parse_filename(path) for path in directory.rglob('*.wav')]
    if not samples:
        raise RuntimeError(f"No audio files found in {directory}")
    samples.sort(key=lambda sample: sample.path.name)
    random.shuffle(samples)
    return samples


class AudioEmotionDataset(Dataset):
    def __init__(self, samples: Iterable[AudioSample], max_frames: int = 200) -> None:
        self.samples = list(samples)
        self.max_frames = max_frames

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        sample = self.samples[index]
        features = extract_and_pad(sample.path, self.max_frames)
        tensor = torch.from_numpy(features).unsqueeze(0)  # (1, n_mfcc, frames)
        label_index = torch.tensor(EMOTION_INDEX[sample.emotion], dtype=torch.long)
        lie_score = torch.tensor(sample.lie_label, dtype=torch.float32)
        return tensor, label_index, lie_score


def split_samples(samples: List[AudioSample], train_ratio: float = 0.8) -> Tuple[List[AudioSample], List[AudioSample]]:
    count = len(samples)
    cutoff = int(count * train_ratio)
    return samples[:cutoff], samples[cutoff:]
