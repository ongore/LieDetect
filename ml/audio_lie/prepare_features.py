from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from tqdm import tqdm

from .config import config
from .dataset import load_dataset
from .features import extract_and_pad


def prepare() -> Path:
    samples = load_dataset(config.raw_dataset_dir)
    features = []
    labels = []
    for sample in tqdm(samples, desc='Extracting MFCC', unit='file'):
        features.append(extract_and_pad(sample.path))
        labels.append({
            'path': str(sample.path),
            'emotion': sample.emotion,
            'lie_label': sample.lie_label
        })

    feature_array = np.stack(features)
    npz_path = config.processed_dir / 'audio_features.npz'
    np.savez_compressed(npz_path, features=feature_array, metadata=labels)

    meta_path = config.processed_dir / 'audio_metadata.json'
    meta_path.write_text(json.dumps(labels, indent=2), encoding='utf-8')
    return npz_path


if __name__ == '__main__':
    output = prepare()
    print(f'Saved features to {output}')
