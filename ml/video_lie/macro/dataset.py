from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

from ..config import config

EMOTION_LABELS = {
    0: 'angry',
    1: 'disgust',
    2: 'fearful',
    3: 'happy',
    4: 'sad',
    5: 'surprised',
    6: 'neutral'
}


class Fer2013Dataset(Dataset):
    def __init__(self, csv_path: Path, usage: str = 'Training') -> None:
        if not csv_path.exists():
            raise FileNotFoundError(f"FER2013 csv not found at {csv_path}")
        df = pd.read_csv(csv_path)
        subset = df[df['Usage'] == usage]
        self.pixels = subset['pixels'].tolist()
        self.labels = subset['emotion'].tolist()

    def __len__(self) -> int:
        return len(self.pixels)

    def __getitem__(self, index: int) -> Tuple[torch.Tensor, torch.Tensor]:
        pixel_array = np.fromstring(self.pixels[index], dtype=np.float32, sep=' ')
        image = pixel_array.reshape(48, 48) / 255.0
        image = np.stack([image, image, image], axis=0)  # convert to 3 channels
        image = torch.from_numpy(image)
        label = torch.tensor(self.labels[index], dtype=torch.long)
        return image, label
