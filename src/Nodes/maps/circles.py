from src.Nodes.maps.utils.Geos import get_polar
import torch
import math
from src.Nodes.maps.point_map import PointMap
from src.Nodes.node_socket import NodeSocket


class Circles(PointMap):

    def __init__(self, node_id):
        self.noso_points = NodeSocket(False, "Points", None)
        self.noso_rotation = NodeSocket(False, "Rotation", None)
        self.noso_frequency = NodeSocket(False, "Frequency", None)
        self.noso_weights_rad = NodeSocket(False, "Weights", None)
        self.noso_scale = NodeSocket(False, "Scale", None)
        self.noso_shift = NodeSocket(False, "Shift", None)
        self.noso_ratio = NodeSocket(False, "Ratio", None)

        self.angle_space = None

        super().__init__(node_id, "Circles", [
            self.noso_points,
            self.noso_rotation,
            self.noso_frequency,
            self.noso_weights_rad,
            self.noso_scale,
            self.noso_shift,
            self.noso_ratio
        ])

    def produce(self):
        rad_out = None
        points = self.noso_points.get().produce()
        weights_rad = self.noso_weights_rad.get().produce()
        weights_rad = weights_rad / torch.sum(weights_rad)
        for i in range(points.shape[0]):
            rad, _ = get_polar(self.width, self.height, self.device, points[i])
            rad = rad / math.sqrt((self.width/2)**2 + (self.height/2)**2) * weights_rad[i]
            if rad_out is None:
                rad_out = rad
            else:
                rad_out += rad

        rad_out = (rad_out * self.noso_scale.get().produce() + self.noso_shift.get().produce()) % 1

        arr_map = rad_out

        return arr_map
