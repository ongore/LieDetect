from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List

import cv2
import mediapipe as mp
import numpy as np


mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)


@dataclass
class MicroFeatures:
    landmark_deltas: np.ndarray
    eye_aspect_ratio_variance: float
    brow_lift_variance: float


def extract_micro_features(video_path: Path, frame_step: int = 2) -> MicroFeatures:
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"Failed to open video: {video_path}")

    previous_landmarks: np.ndarray | None = None
    deltas: List[np.ndarray] = []
    ear_values: List[float] = []
    brow_values: List[float] = []
    frame_index = 0

    while True:
        success, frame = capture.read()
        if not success:
            break
        if frame_index % frame_step != 0:
            frame_index += 1
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = mp_face_mesh.process(rgb)
        if not result.multi_face_landmarks:
            frame_index += 1
            continue
        landmarks = np.array([(lm.x, lm.y, lm.z) for lm in result.multi_face_landmarks[0].landmark])

        if previous_landmarks is not None:
            deltas.append(landmarks - previous_landmarks)
            ear_values.append(_eye_aspect_ratio(landmarks))
            brow_values.append(_brow_distance(landmarks))

        previous_landmarks = landmarks
        frame_index += 1

    capture.release()

    if not deltas:
        deltas.append(np.zeros((468, 3)))
    landmark_deltas = np.mean(np.abs(np.stack(deltas)), axis=0).flatten()
    ear_variance = float(np.var(ear_values)) if ear_values else 0.0
    brow_variance = float(np.var(brow_values)) if brow_values else 0.0

    return MicroFeatures(
        landmark_deltas=landmark_deltas.astype(np.float32),
        eye_aspect_ratio_variance=ear_variance,
        brow_lift_variance=brow_variance
    )


def _eye_aspect_ratio(landmarks: np.ndarray) -> float:
    left_indices = [33, 160, 158, 133, 153, 144]
    right_indices = [362, 385, 387, 263, 373, 380]
    return _aspect_ratio(landmarks, left_indices) + _aspect_ratio(landmarks, right_indices)


def _brow_distance(landmarks: np.ndarray) -> float:
    brow_indices = [70, 63, 105, 66, 107]
    eye_indices = [33, 133, 362, 263]
    brow_avg = np.mean(landmarks[brow_indices], axis=0)
    eye_avg = np.mean(landmarks[eye_indices], axis=0)
    return float(np.linalg.norm(brow_avg - eye_avg))


def _aspect_ratio(landmarks: np.ndarray, indices: List[int]) -> float:
    p2 = landmarks[indices[1]]
    p6 = landmarks[indices[5]]
    p3 = landmarks[indices[2]]
    p5 = landmarks[indices[4]]
    p1 = landmarks[indices[0]]
    p4 = landmarks[indices[3]]
    vertical = np.linalg.norm(p2 - p6) + np.linalg.norm(p3 - p5)
    horizontal = np.linalg.norm(p1 - p4)
    if horizontal == 0:
        return 0.0
    return vertical / (2.0 * horizontal)
