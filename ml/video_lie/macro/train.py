from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms
from tqdm import tqdm

from ..config import config
from .dataset import Fer2013Dataset
from .model import create_macro_model


def train(csv_path: Path) -> Dict[str, float]:
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    transform = transforms.Compose([
        transforms.Resize((config.image_size, config.image_size)),
        transforms.RandomHorizontalFlip(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])

    train_dataset = Fer2013Dataset(csv_path, usage='Training')
    val_dataset = Fer2013Dataset(csv_path, usage='PublicTest')

    train_loader = DataLoader(train_dataset, batch_size=config.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=config.batch_size)

    model = create_macro_model().to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = nn.CrossEntropyLoss()

    best_val_acc = 0.0
    history: Dict[str, float] = {}

    for epoch in range(1, config.num_epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for inputs, labels in tqdm(train_loader, desc=f"Macro epoch {epoch}", leave=False):
            inputs = transform(inputs).to(device)
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
        val_loss, val_acc = evaluate(model, val_loader, criterion, transform, device)
        history[f'epoch_{epoch}'] = {
            'train_loss': train_loss,
            'train_acc': train_acc,
            'val_loss': val_loss,
            'val_acc': val_acc
        }

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            save_path = config.processed_dir / 'macro_resnet.pt'
            torch.save({'model_state_dict': model.state_dict(), 'val_acc': val_acc}, save_path)

    metrics = {'best_val_acc': best_val_acc}
    history_path = config.processed_dir / 'macro_history.json'
    history_path.write_text(json.dumps(history, indent=2), encoding='utf-8')
    return metrics


def evaluate(model: nn.Module, loader: DataLoader, criterion: nn.Module, transform, device) -> tuple[float, float]:
    model.eval()
    total_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in loader:
            inputs = transform(inputs).to(device)
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
    csv = Path('data/raw/fer2013/fer2013.csv')
    metrics = train(csv)
    print(json.dumps(metrics, indent=2))
