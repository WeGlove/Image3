from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch


class Uniform(Node):

    def __init__(self):
        super().__init__([], [], "Returns the given value.")

    def produce(self):
        return torch.rand((self.defaults.width, self.defaults.height), device=self.defaults.device)
