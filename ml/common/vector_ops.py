from __future__ import annotations

from typing import Iterable, List

from .emotions import EMOTION_TO_INDEX


def expand_emotion_vector(labels: Iterable[str], probabilities: Iterable[float]) -> List[float]:
    vector = [0.0] * len(EMOTION_TO_INDEX)
    for label, prob in zip(labels, probabilities):
        if label in EMOTION_TO_INDEX:
            vector[EMOTION_TO_INDEX[label]] = float(prob)
    return vector
