import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class RFFT(Node):

    def __init__(self):
        self.input = NodeSocket("Map")
        super().__init__([self.input])

    def produce(self):
        mask = self.input.get().produce()
        fft = torch.fft.rfft2(mask)

        return fft
