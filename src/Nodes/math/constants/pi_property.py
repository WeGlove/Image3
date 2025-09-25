import math
from src.Nodes.node import Node
import torch


class PiProperty(Node):

    def __init__(self):
        super().__init__([], [], "Returns Pi")

    def produce(self):
        return torch.tensor(math.pi)
