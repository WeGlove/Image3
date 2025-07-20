import torch
from src.Nodes.node_socket import NodeSocket
from src.Nodes.node import Node
from src.math.color import rgb_to_hsv


class RGBToG(Node):

    def __init__(self):
        self.rgb = NodeSocket("RGB")
        super().__init__([self.rgb])

    def produce(self):
        img = self.rgb.get().produce()

        return img[:, :, 1]
