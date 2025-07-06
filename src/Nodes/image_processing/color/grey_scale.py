import torch
from src.math.color import grey_scale
from src.Nodes.node_socket import NodeSocket
from src.Nodes.node import Node


class GreyScale(Node):

    def __init__(self):
        self.R = NodeSocket("R")
        self.G = NodeSocket("G")
        self.B = NodeSocket("B")
        self.shift = NodeSocket("Shift")

        super().__init__([self.R, self.G, self.B, self.shift],
                         [], "Coloring")

    def produce(self):
        grey_mask = grey_scale(self.R.get().produce(), self.G.get().produce(), self.B.get().produce())
        return grey_mask
