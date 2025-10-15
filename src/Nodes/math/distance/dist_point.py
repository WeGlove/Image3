from src.math.gemoetry import get_polar
import math
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.Nodes.internal.internal_value import InternalValue


class DistPoint(Node):

    def __init__(self):
        self.noso_point = NodeSocket("Point")
        self.noso_scale = NodeSocket("Scale", default=InternalValue(1))
        self.noso_shift = NodeSocket("Shift", default=InternalValue(0))

        self.angle_space = None

        super().__init__([
            self.noso_point,
            self.noso_scale,
            self.noso_shift,
        ], [], "DistPoint")

    def produce(self):
        point = self.noso_point.get().produce()
        rad, _ = get_polar(self.defaults.width, self.defaults.height, self.defaults.device, point)
        rad = rad / math.sqrt((self.defaults.width/2)**2 + (self.defaults.height/2)**2)

        rad_out = (rad * self.noso_scale.get().produce() + self.noso_shift.get().produce()) % 1

        return rad_out
