import torch
from src.Nodes.node_socket import NodeSocket
from src.Nodes.node import Node
from src.math.color import rgb_to_hsv


class TensorsToRGB(Node):

    def __init__(self):
        self.r = NodeSocket("R")
        self.g = NodeSocket("G")
        self.b = NodeSocket("B")
        super().__init__([self.r, self.g, self.b])

    def produce(self):
        img = torch.stack([self.r.get().produce(), self.g.get().produce(), self.b.get().produce()])
        img = torch.reshape(img, (img.shape[1], img.shape[2], img.shape[0]))

        return img
