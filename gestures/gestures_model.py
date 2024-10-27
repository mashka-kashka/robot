from torch import nn
import torch.nn.functional as F


class GesturesNet(nn.Module):
    def __init__(self, labels):
        super().__init__()
        self.labels = labels
        self.fc1 = nn.Linear(64, 32).double()
        self.fc2 = nn.Linear(32, 16).double()
        self.fc3 = nn.Linear(16, len(labels)).double()

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.softmax(self.fc3(x))
        return x