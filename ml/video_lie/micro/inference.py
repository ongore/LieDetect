from __future__ import annotations

from pathlib import Path
from typing import Dict

import numpy as np

from ..config import config
from .features import extract_micro_features


def load_micro_model(model_path: Path | None = None) -> Dict[str, np.ndarray]:
    path = model_path or (config.processed_dir / 'micro_model.npz')
    if not path.exists():
        raise FileNotFoundError(f"Micro model weights not found: {path}")
    data = np.load(path, allow_pickle=True)
    return {
        'coef': data['coef'],
        'intercept': data['intercept'],
        'scaler_mean': data['scaler_mean'],
        'scaler_scale': data['scaler_scale']
    }


def predict_lie_score(video_path: Path, model_assets: Dict[str, np.ndarray]) -> float:
    features = extract_micro_features(video_path)
    vector = np.concatenate([
        features.landmark_deltas,
        np.array([features.eye_aspect_ratio_variance, features.brow_lift_variance], dtype=np.float32)
    ])
    vector = (vector - model_assets['scaler_mean']) / model_assets['scaler_scale']
    logits = vector.dot(model_assets['coef'].T) + model_assets['intercept']
    prob = 1 / (1 + np.exp(-logits))
    return float(prob.squeeze())
