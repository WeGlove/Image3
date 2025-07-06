import torch
from src.Nodes.node import Node


class EdgeDetection(Node):

    def __init__(self):
        self.reader = None
        super().__init__(description="Edge Detection")

    def produce(self):
        mask = torch.tensor([
            [-1, -1, -1],
            [-1, 8, -1],
            [-1, -1, -1]
        ], device=self.defaults.device, dtype=torch.float)
        return mask

