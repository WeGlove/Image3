import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Constant(Node):

    def __init__(self):
        self.constant = NodeSocket("Constant")
        super().__init__([self.constant], [], "Power")

    def produce(self):
        gradient = torch.ones(self.defaults.width) * self.constant.get().produce()
        return gradient
