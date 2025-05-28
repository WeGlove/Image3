from src.Nodes.maps.utils.Geos import get_polar
import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Polar(Node):

    def __init__(self):
        self.center = NodeSocket(False, "Center", None)
        self.angle_shift = NodeSocket(False, "Angle Shit", None)
        super().__init__([self.center, self.angle_shift])

    def produce(self):
        radius, angle = get_polar(self.width, self.height, self.device, self.center.get().produce())
        angle = (angle / torch.pi + 1) / 2
        angle += self.angle_shift.get().produce()
        angle %= 1

        return torch.stack([radius, angle])
