from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch


class Abs(Node):

    def __init__(self):
        self.input_noso = NodeSocket("Input", None)
        super().__init__([self.input_noso])
        super().__init__([], [], "Returns the given value.")

    def produce(self):
        return torch.abs(self.input_noso.get().produce())
