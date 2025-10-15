from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch


class Reshape(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.shape = NodeSocket("Shape")
        super().__init__([self.a, self.shape], [], "Division")

    def produce(self):
        return torch.reshape(self.a.get().produce(), list(self.shape.get().produce()))
