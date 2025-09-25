import torch
from src.Nodes.node import Node


class RowRange(Node):

    def __init__(self):
        super().__init__()

    def produce(self):
        return torch.linspace(-1, 1, self.defaults.width)
