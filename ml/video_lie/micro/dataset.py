from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

import numpy as np
import torch
from torch.utils.data import Dataset

from .features import MicroFeatures, extract_micro_features


@dataclass
class MicroSample:
    video_path: Path
    label: int  # 1 for lie, 0 for truth


def load_manifest(manifest_path: Path) -> List[MicroSample]:
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")
    entries = json.loads(manifest_path.read_text(encoding='utf-8'))
    samples: List[MicroSample] = []
    for entry in entries:
        samples.append(MicroSample(video_path=Path(entry['video']), label=int(entry['label'])))
    return samples


class MicroExpressionDataset(Dataset):
    def __init__(self, manifest_path: Path, cache_dir: Path | None = None) -> None:
        self.samples = load_manifest(manifest_path)
        self.cache_dir = cache_dir
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        sample = self.samples[index]
        features = self._load_or_compute(sample.video_path)
        feature_tensor = torch.from_numpy(features)
        label = torch.tensor(sample.label, dtype=torch.float32)
        return feature_tensor, label

    def _load_or_compute(self, path: Path) -> np.ndarray:
        if self.cache_dir:
            cache_file = self.cache_dir / f"{path.stem}.npy"
            if cache_file.exists():
                return np.load(cache_file)
        micro = extract_micro_features(path)
        combined = np.concatenate([
            micro.landmark_deltas,
            np.array([micro.eye_aspect_ratio_variance, micro.brow_lift_variance], dtype=np.float32)
        ])
        if self.cache_dir:
            np.save(cache_file, combined)
        return combined
