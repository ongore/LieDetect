from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict

import boto3
import torch

from ..constants import BAD_EMOTIONS, EMOTION_INDEX
from ..features import extract_and_pad
from ..model import AudioEmotionNet


def model_fn(model_dir: str) -> AudioEmotionNet:
    model = AudioEmotionNet(num_emotions=len(EMOTION_INDEX))
    weights_path = Path(model_dir) / 'model.pt'
    if weights_path.exists():
        state = torch.load(weights_path, map_location='cpu')
        model.load_state_dict(state['model_state_dict'])
    model.eval()
    return model


def input_fn(serialized_input: str, content_type: str) -> Dict[str, Any]:
    if content_type == 'application/json':
        return json.loads(serialized_input)
    raise ValueError(f"Unsupported content type: {content_type}")


def predict_fn(data: Dict[str, Any], model: AudioEmotionNet) -> Dict[str, Any]:
    bucket = data.get('bucket') or os.environ.get('DEFAULT_AUDIO_BUCKET')
    key = data.get('audioKey') or data.get('videoKey')
    if not bucket or not key:
        raise ValueError('bucket and audioKey/videoKey are required')

    with tempfile.TemporaryDirectory() as tmpdir:
        local_path = Path(tmpdir) / 'input.wav'
        _download_from_s3(bucket, key, local_path)
        features = extract_and_pad(local_path)

    tensor = torch.from_numpy(features).unsqueeze(0).unsqueeze(0)
    with torch.no_grad():
        probs = model.predict_emotion_vector(tensor).squeeze(0)

    lie_score = _compute_lie_score(probs)
    return {
        'emotion_vector': probs.tolist(),
        'lie_score': lie_score
    }


def output_fn(prediction: Dict[str, Any], accept: str) -> str:
    if accept == 'application/json':
        return json.dumps(prediction)
    raise ValueError(f"Unsupported accept type: {accept}")


def _download_from_s3(bucket: str, key: str, destination: Path) -> None:
    s3 = boto3.client('s3')
    destination.parent.mkdir(parents=True, exist_ok=True)
    s3.download_file(bucket, key, str(destination))


def _compute_lie_score(vector: torch.Tensor) -> float:
    emotions = sorted(EMOTION_INDEX.keys())
    score = 0.0
    for idx, emotion in enumerate(emotions):
        weight = 1.0 if emotion in BAD_EMOTIONS else 0.5
        score += weight * float(vector[idx])
    max_score = len(BAD_EMOTIONS) * 1.0 + (len(emotions) - len(BAD_EMOTIONS)) * 0.5
    return round(score / max_score, 4)
