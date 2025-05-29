from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch
from torch.nn.functional import conv2d


class Convolution(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.b = NodeSocket("B")
        self.reader = None
        super().__init__([self.a, self.b], [], "Convolution")

    def produce(self):
        a = self.a.get().produce()
        a = torch.reshape(a, (1, 1, *a.shape))
        b = self.b.get().produce()
        b = torch.reshape(b, (1, 1, *b.shape))
        mask = conv2d(a, b, padding="same")
        mask = mask[0][0]
        return mask
