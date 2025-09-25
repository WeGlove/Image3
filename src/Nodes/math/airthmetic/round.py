from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch
from src.Nodes.system.internal_value import InternalValue


class Round(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.k = NodeSocket("Bin Size", default=InternalValue(1))
        self.shift = NodeSocket("Shift", default=InternalValue(0))
        super().__init__([self.a, self.k, self.shift], [], "Round")

    def produce(self):
        a = self.a.get().produce()
        k = self.k.get().produce()
        shift = self.shift.get().produce()

        if torch.is_complex(a):
            a.imag = torch.floor(a.imag / k + shift) * k
            a.real = torch.floor(a.real / k + shift) * k
        else:
            a = torch.floor(a / k + shift) * k

        return a
