from __future__ import annotations

from pathlib import Path
from typing import Dict

import torch
from PIL import Image
from torchvision import transforms

from ..config import config
from ml.common.vector_ops import expand_emotion_vector
from .dataset import EMOTION_LABELS
from .model import create_macro_model, emotion_vector


def load_macro_model(weights_path: Path | None = None) -> torch.nn.Module:
    model = create_macro_model()
    path = weights_path or config.processed_dir / 'macro_resnet.pt'
    if path.exists():
        state = torch.load(path, map_location='cpu')
        model.load_state_dict(state['model_state_dict'])
    model.eval()
    return model


def analyze_frame(image_path: Path, model: torch.nn.Module | None = None) -> Dict[str, object]:
    model = model or load_macro_model()
    transform = transforms.Compose([
        transforms.Resize((config.image_size, config.image_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    image = Image.open(image_path).convert('RGB')
    tensor = transform(image).unsqueeze(0)
    probabilities = emotion_vector(model, tensor).squeeze(0)
    labels = [EMOTION_LABELS[idx] for idx in range(len(probabilities))]
    canonical_vector = expand_emotion_vector(labels, probabilities.tolist())
    return {
        'emotion_vector': canonical_vector,
        'max_emotion_index': int(torch.argmax(probabilities).item())
    }
