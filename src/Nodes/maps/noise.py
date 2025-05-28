import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Noise(Node):

    def __init__(self):
        self.bias = NodeSocket(False, "Bias", default=None, description="")
        super().__init__([self.bias])

    def produce(self):
        noise_map = torch.rand(self.width, self.height, device=self.device) ** self.bias.get().produce()
        return noise_map
