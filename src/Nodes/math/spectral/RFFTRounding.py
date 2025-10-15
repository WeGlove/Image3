import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.Nodes.internal.internal_value import InternalValue
from src.math.bin_round import bin_round


class RFFTRounding(Node):

    def __init__(self):
        self.input = NodeSocket("Map")
        self.k = NodeSocket("Bin Size", default=InternalValue(1))
        self.shift = NodeSocket("Shift", default=InternalValue(0))
        super().__init__([self.input, self.k, self.shift])

    def produce(self):
        mask = self.input.get().produce()
        fft = torch.fft.rfft2(mask)

        k = self.k.get().produce()
        shift = self.shift.get().produce()

        fft = bin_round(fft, k, shift)
        mask = torch.fft.irfft2(fft)

        return mask
