from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch


class Uniform(Node):

    def __init__(self):
        self.noso_width = NodeSocket("Width")
        self.noso_height = NodeSocket("Height")
        super().__init__([self.noso_width, self.noso_height], [], "Returns the given value.")

    def produce(self):
        return torch.rand((self.noso_width.get().produce(), self.noso_height.get().produce()))
