from __future__ import annotations

from pathlib import Path
from typing import Tuple

import librosa
import numpy as np

from .config import config


def extract_mfcc(path: Path) -> np.ndarray:
    signal, _ = librosa.load(path, sr=config.sample_rate)
    mfcc = librosa.feature.mfcc(
        y=signal,
        sr=config.sample_rate,
        n_mfcc=config.n_mfcc,
        n_fft=config.frame_length,
        hop_length=config.hop_length
    )
    # Normalize per-coefficient
    mfcc = (mfcc - np.mean(mfcc, axis=1, keepdims=True)) / (np.std(mfcc, axis=1, keepdims=True) + 1e-8)
    return mfcc.astype(np.float32)


def pad_features(features: np.ndarray, max_frames: int = 200) -> np.ndarray:
    if features.shape[1] >= max_frames:
        return features[:, :max_frames]
    pad_width = max_frames - features.shape[1]
    return np.pad(features, ((0, 0), (0, pad_width)), mode='constant')


def extract_and_pad(path: Path, max_frames: int = 200) -> np.ndarray:
    mfcc = extract_mfcc(path)
    return pad_features(mfcc, max_frames)
