import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class iRFFT(Node):

    def __init__(self):
        self.input = NodeSocket("Map")
        super().__init__([self.input])

    def produce(self):
        fft = self.input.get().produce()
        mask = torch.fft.irfft2(fft)

        return mask
