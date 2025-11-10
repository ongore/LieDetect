from __future__ import annotations

from pathlib import Path
from typing import Dict

import torch

from .config import config
from .constants import BAD_EMOTIONS, EMOTION_INDEX
from .dataset import parse_filename
from .features import extract_and_pad
from .model import AudioEmotionNet


def load_model(weights_path: Path | None = None) -> AudioEmotionNet:
    model = AudioEmotionNet(num_emotions=len(EMOTION_INDEX))
    path = weights_path or config.processed_dir / 'audio_emotion_net.pt'
    if path.exists():
        state = torch.load(path, map_location='cpu')
        model.load_state_dict(state['model_state_dict'])
    model.eval()
    return model


def emotion_vector_from_audio(path: Path, model: AudioEmotionNet | None = None) -> torch.Tensor:
    model = model or load_model()
    features = extract_and_pad(path)
    tensor = torch.from_numpy(features).unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        probs = model.predict_emotion_vector(tensor)
    return probs.squeeze(0)


def compute_lie_score(vector: torch.Tensor) -> float:
    emotion_list = sorted(EMOTION_INDEX.keys())
    score = 0.0
    for idx, emotion in enumerate(emotion_list):
        weight = 1.0 if emotion in BAD_EMOTIONS else 0.5
        score += weight * float(vector[idx])
    max_score = len(BAD_EMOTIONS) * 1.0 + (len(emotion_list) - len(BAD_EMOTIONS)) * 0.5
    return round(score / max_score, 4)


def analyze_file(path: Path) -> Dict[str, object]:
    model = load_model()
    vector = emotion_vector_from_audio(path, model)
    lie_score = compute_lie_score(vector)
    metadata = parse_filename(path)
    return {
        'emotion_vector': vector.tolist(),
        'lie_score': lie_score,
        'metadata': {
            'emotion': metadata.emotion,
            'intensity': metadata.intensity,
            'actor': metadata.actor,
            'lie_label': metadata.lie_label
        }
    }
