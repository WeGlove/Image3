from src.math.gemoetry import get_polar
import torch
import math
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Circles(Node):

    def __init__(self):
        self.noso_points = NodeSocket("Points")
        self.noso_rotation = NodeSocket("Rotation")
        self.noso_frequency = NodeSocket("Frequency")
        self.noso_weights_rad = NodeSocket("Weights")
        self.noso_scale = NodeSocket("Scale")
        self.noso_shift = NodeSocket("Shift")
        self.noso_ratio = NodeSocket("Ratio")

        self.angle_space = None

        super().__init__([
            self.noso_points,
            self.noso_rotation,
            self.noso_frequency,
            self.noso_weights_rad,
            self.noso_scale,
            self.noso_shift,
            self.noso_ratio
        ], [], "Circles")

    def produce(self):
        rad_out = None
        points = self.noso_points.get().produce()
        weights_rad = self.noso_weights_rad.get().produce()
        weights_rad = weights_rad / torch.sum(weights_rad)
        for i in range(points.shape[0]):
            rad, _ = get_polar(self.defaults.width, self.defaults.height, self.defaults.device, points[i])
            rad = rad / math.sqrt((self.defaults.width/2)**2 + (self.defaults.height/2)**2) * weights_rad[i]
            if rad_out is None:
                rad_out = rad
            else:
                rad_out += rad

        rad_out = (rad_out * self.noso_scale.get().produce() + self.noso_shift.get().produce()) % 1

        arr_map = rad_out

        return arr_map
