from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm

from .config import config
from .constants import BAD_EMOTIONS, EMOTION_INDEX
from .dataset import AudioEmotionDataset, load_dataset, split_samples
from .model import AudioEmotionNet


def train() -> Dict[str, float]:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    samples = load_dataset(config.raw_dataset_dir)
    train_samples, val_samples = split_samples(samples)

    train_loader = DataLoader(AudioEmotionDataset(train_samples), batch_size=config.batch_size, shuffle=True)
    val_loader = DataLoader(AudioEmotionDataset(val_samples), batch_size=config.batch_size)

    model = AudioEmotionNet(num_emotions=len(EMOTION_INDEX)).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = nn.CrossEntropyLoss()

    best_val_acc = 0.0
    history: Dict[str, float] = {}

    for epoch in range(1, config.num_epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels, _ in tqdm(train_loader, desc=f"Epoch {epoch} train", leave=False):
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += inputs.size(0)

        train_loss = running_loss / total
        train_acc = correct / total

        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        history[f'epoch_{epoch}'] = {
            'train_loss': train_loss,
            'train_acc': train_acc,
            'val_loss': val_loss,
            'val_acc': val_acc
        }

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            save_path = config.processed_dir / 'audio_emotion_net.pt'
            torch.save({'model_state_dict': model.state_dict(), 'val_acc': val_acc}, save_path)

    metrics = {
        'best_val_acc': best_val_acc,
        'num_samples': len(samples)
    }
    history_path = config.processed_dir / 'audio_training_history.json'
    history_path.write_text(json.dumps(history, indent=2), encoding='utf-8')
    return metrics


def evaluate(model: AudioEmotionNet, loader: DataLoader, criterion: nn.Module, device: torch.device) -> tuple[float, float]:
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels, _ in loader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            total_loss += loss.item() * inputs.size(0)
            preds = outputs.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += inputs.size(0)

    if total == 0:
        return 0.0, 0.0
    return total_loss / total, correct / total


if __name__ == '__main__':
    metrics = train()
    print(json.dumps(metrics, indent=2))
