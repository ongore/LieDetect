from __future__ import annotations

from typing import Dict, Iterable, List, Sequence

from ml.common.emotions import EMOTION_TO_INDEX


def average_vectors(vectors: Iterable[Sequence[float]]) -> List[float]:
    vectors = list(vectors)
    if not vectors:
        return [0.0] * len(EMOTION_TO_INDEX)
    length = len(EMOTION_TO_INDEX)
    totals = [0.0] * length
    for vector in vectors:
        if len(vector) != length:
            raise ValueError("Vectors must align with canonical emotion schema")
        for idx, value in enumerate(vector):
            totals[idx] += value
    count = float(len(vectors))
    return [round(total / count, 4) for total in totals]


def cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    if len(vec_a) != len(vec_b):
        raise ValueError("Vectors must have the same length")
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = sum(a * a for a in vec_a) ** 0.5
    norm_b = sum(b * b for b in vec_b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return round(dot / (norm_a * norm_b), 4)


def fuse_lie_scores(audio: float, macro: float, micro: float, weights: Sequence[float] | None = None) -> float:
    weights = list(weights or (0.35, 0.35, 0.30))
    total = sum(weights)
    normalized = [w / total for w in weights]
    fused = audio * normalized[0] + macro * normalized[1] + micro * normalized[2]
    return round(fused, 4)


def llm_alignment_score(emotion_vector: Sequence[float], llm_vector: Dict[str, float]) -> float:
    llm_list = [llm_vector.get(emotion, 0.0) for emotion in EMOTION_TO_INDEX]
    return cosine_similarity(emotion_vector, llm_list)


def final_lie_score(micro_score: float, alignment_score: float) -> float:
    mismatch = 1 - max(alignment_score, 0.0)
    return round((mismatch + micro_score) / 2, 4)
