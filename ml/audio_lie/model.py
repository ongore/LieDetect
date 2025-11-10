from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

from .constants import EMOTION_INDEX


class AudioEmotionNet(nn.Module):
    def __init__(self, num_emotions: int = len(EMOTION_INDEX)) -> None:
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=(3, 3), padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=(3, 3), padding=1)
        self.bn2 = nn.BatchNorm2d(32)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=(3, 3), padding=1)
        self.bn3 = nn.BatchNorm2d(64)
        self.dropout = nn.Dropout(0.3)
        self.fc1 = nn.Linear(64, 256)
        self.fc2 = nn.Linear(256, num_emotions)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.max_pool2d(x, kernel_size=(1, 2))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.max_pool2d(x, kernel_size=(2, 2))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.adaptive_avg_pool2d(x, (1, 1))
        x = x.view(x.size(0), -1)
        x = self.dropout(F.relu(self.fc1(x)))
        logits = self.fc2(x)
        return logits

    def predict_emotion_vector(self, x: torch.Tensor) -> torch.Tensor:
        logits = self.forward(x)
        return torch.softmax(logits, dim=1)
