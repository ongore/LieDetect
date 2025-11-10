from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from ..config import config
from .dataset import MicroExpressionDataset


def train(manifest_path: Path, cache_dir: Path | None = None) -> Dict[str, float]:
    dataset = MicroExpressionDataset(manifest_path, cache_dir)
    features, labels = _stack_dataset(dataset)

    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    clf = LogisticRegression(max_iter=500)
    clf.fit(x_train, y_train)

    preds = clf.predict(x_test)
    proba = clf.predict_proba(x_test)[:, 1]

    metrics = {
        'accuracy': float(accuracy_score(y_test, preds)),
        'roc_auc': float(roc_auc_score(y_test, proba)),
        'samples': int(len(dataset))
    }

    model_path = config.processed_dir / 'micro_model.npz'
    model_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(model_path, coef=clf.coef_, intercept=clf.intercept_, scaler_mean=scaler.mean_, scaler_scale=scaler.scale_)

    metrics_path = config.processed_dir / 'micro_metrics.json'
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding='utf-8')
    return metrics


def _stack_dataset(dataset: MicroExpressionDataset) -> Tuple[np.ndarray, np.ndarray]:
    features = []
    labels = []
    for feature_tensor, label_tensor in dataset:
        features.append(feature_tensor.numpy())
        labels.append(label_tensor.item())
    return np.vstack(features), np.array(labels)


if __name__ == '__main__':
    manifest = Path('data/raw/micro/manifest.json')
    stats = train(manifest, cache_dir=config.processed_dir / 'micro_cache')
    print(json.dumps(stats, indent=2))
