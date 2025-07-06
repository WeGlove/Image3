from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch


class Matmul(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.b = NodeSocket("B")
        self.reader = None
        super().__init__([self.a, self.b], [], "Matmul")

    def produce(self):
        return torch.matmul(self.a.get().produce(), self.b.get().produce())
