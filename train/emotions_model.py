from torch import nn
import torch.nn.functional as F
from mediapipe.python.solutions.face_mesh import FACEMESH_NUM_LANDMARKS_WITH_IRISES


class EmotionsNet(nn.Module):

        def __init__(self, labels):
            super().__init__()
            self.dim = len(labels)
            self.labels = labels
            self.fc1 = nn.Linear(FACEMESH_NUM_LANDMARKS_WITH_IRISES * 3, 1024).double()
            self.fc2 = nn.Linear(1024, 512).double()
            self.fc3 = nn.Linear(512, 256).double()
            self.fc4 = nn.Linear(256, self.dim).double()

        def forward(self, x):
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = F.relu(self.fc3(x))
            x = F.softmax(self.fc4(x), dim=1)
            return x

        def get_emotion(self, prediction):
            return self.labels[prediction.argmax()]