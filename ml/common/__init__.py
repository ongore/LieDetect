"""Common constants and vector utilities for ML components."""

from .emotions import EMOTION_TO_INDEX  # noqa: F401
from .vector_ops import expand_emotion_vector  # noqa: F401

__all__ = ["EMOTION_TO_INDEX", "expand_emotion_vector"]

