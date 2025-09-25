from src.math.gemoetry import get_polar
import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Polar(Node):

    def __init__(self):
        self.center = NodeSocket("Center")
        self.angle_shift = NodeSocket("Angle Shift")
        super().__init__([self.center, self.angle_shift])

    def produce(self):
        radius, angle = get_polar(self.defaults.width, self.defaults.height, self.defaults.device,
                                  self.center.get().produce())
        angle = (angle / torch.pi + 1) / 2
        angle += self.angle_shift.get().produce()
        angle %= 1

        return torch.stack([radius, angle])
