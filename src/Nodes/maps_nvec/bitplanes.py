import torch
from src.Nodes.node_socket import NodeSocket
from src.Nodes.node import Node


class BitPlanes(Node):

    def __init__(self):
        self.input = NodeSocket(False, "Input", default=None, description="")
        super().__init__([self.input])

    def produce(self):
        mask = self.input.get().produce()
        mask = torch.tensor(mask, dtype=torch.int8)

        bitplanes = []
        for i in range(8):
            bitplane = mask % 2
            mask = mask >> 1
            bitplanes.append(bitplane)

        return torch.tensor(bitplanes, device=self.device)
