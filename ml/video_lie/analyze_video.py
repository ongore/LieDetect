from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import numpy as np

from ml.common.vector_ops import expand_emotion_vector
from ml.common.emotions import EMOTIONS
from .config import config
from .frame_extractor import extract_frames
from .macro.inference import analyze_frame, load_macro_model
from .micro.inference import load_micro_model, predict_lie_score


def analyze_video(
    video_path: Path,
    macro_weights: Path | None = None,
    micro_weights: Path | None = None
) -> Dict[str, object]:
    frames = extract_frames(video_path)
    macro_model = load_macro_model(macro_weights)

    macro_vectors: List[List[float]] = []
    for frame_path in frames:
        result = analyze_frame(frame_path, macro_model)
        macro_vectors.append(result['emotion_vector'])

    if macro_vectors:
        macro_vector = np.mean(np.array(macro_vectors), axis=0).tolist()
    else:
        macro_vector = [0.0] * len(EMOTIONS)

    micro_assets = load_micro_model(micro_weights or (config.processed_dir / 'micro_model.npz'))
    micro_score = predict_lie_score(video_path, micro_assets)

    return {
        'macro_vector': macro_vector,
        'macro_lie_score': float(np.mean(macro_vector)),
        'micro_lie_score': float(micro_score)
    }
