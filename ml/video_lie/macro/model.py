from __future__ import annotations

import torch
import torch.nn as nn
from torchvision import models


def create_macro_model(num_classes: int = 7, pretrained: bool = True) -> nn.Module:
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT if pretrained else None)
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    return model


def emotion_vector(model: nn.Module, inputs: torch.Tensor) -> torch.Tensor:
    model.eval()
    with torch.no_grad():
        logits = model(inputs)
        return torch.softmax(logits, dim=1)
