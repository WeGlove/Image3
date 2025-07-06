import torch
from src.math.color import rgb_to_hsv, hsv_to_rgb
from src.Nodes.node_socket import NodeSocket
from src.Nodes.node import Node


class HueShift(Node):

    def __init__(self):
        self.R = NodeSocket("R")
        self.G = NodeSocket("G")
        self.B = NodeSocket("B")
        self.shift = NodeSocket("Shift")

        super().__init__([self.R, self.G, self.B, self.shift],
                         [], "Coloring")

    def produce(self):
        img = self.img.get().produce()
        H, S, V = rgb_to_hsv(img)
        H = H + self.shift.get().produce()
        R, G, B = hsv_to_rgb(torch.stack([H, S, V]))
        return torch.stack([R, G, B])
