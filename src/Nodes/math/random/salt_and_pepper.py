from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch
from src.Nodes.internal.internal_value import InternalValue


class SaltAndPepper(Node):

    def __init__(self):
        super().__init__()

    def produce(self):
        map = torch.rand((self.defaults.width, self.defaults.height), device=self.defaults.device)
        map = torch.round(map)
        return map
