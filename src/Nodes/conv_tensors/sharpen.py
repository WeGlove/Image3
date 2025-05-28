import torch
from src.Nodes.node import Node


class Sharpen(Node):

    def __init__(self):
        self.reader = None
        super().__init__(description="Mean Tensor")

    def produce(self):
        mask = torch.tensor([
            [0, -1, 0],
            [-1, 5, -1],
            [0, -1, 0]
        ], device=self.device, dtype=torch.float)
        return mask
