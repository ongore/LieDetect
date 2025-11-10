from __future__ import annotations

from pathlib import Path
from typing import List

import cv2

from .config import config


def extract_frames(video_path: Path, output_dir: Path | None = None, fps: int | None = None) -> List[Path]:
    output_dir = output_dir or (config.processed_dir / 'frames' / video_path.stem)
    output_dir.mkdir(parents=True, exist_ok=True)

    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"Failed to open video: {video_path}")

    original_fps = capture.get(cv2.CAP_PROP_FPS) or 30
    target_fps = fps or config.frame_rate
    frame_interval = max(int(original_fps / target_fps), 1)

    frame_idx = 0
    saved_frames: List[Path] = []
    while True:
        success, frame = capture.read()
        if not success:
            break
        if frame_idx % frame_interval == 0:
            resized = cv2.resize(frame, (config.image_size, config.image_size))
            output_path = output_dir / f'{frame_idx:06d}.jpg'
            cv2.imwrite(str(output_path), resized)
            saved_frames.append(output_path)
        frame_idx += 1

    capture.release()
    return saved_frames
