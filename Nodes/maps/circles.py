from Nodes.maps.utils.Geos import get_polar
import torch
from Nodes.system.value_property import ValueProperty
import math
from Nodes.maps.point_map import PointMap
from Nodes.node_socket import NodeSocket


class Circles(PointMap):

    def __init__(self, node_id, device, frame_counter, scale=5, shift=0, ratio=0.5, rotation=0, frequency=1, weights_rad=None):
        self.noso_points = NodeSocket(False, "Points", ValueProperty(None, -1, device=device, frame_counter=frame_counter))
        self.noso_rotation = NodeSocket(False, "Rotation", ValueProperty(rotation, -1, device=device, frame_counter=frame_counter))
        self.noso_frequency = NodeSocket(False, "Frequency", ValueProperty(frequency, -1, device=device, frame_counter=frame_counter))
        self.noso_weights_rad = NodeSocket(False, "Weights", ValueProperty(weights_rad, -1, device=device, frame_counter=frame_counter))
        self.noso_scale = NodeSocket(False, "Scale", ValueProperty(scale, -1, device=device, frame_counter=frame_counter))
        self.noso_shift = NodeSocket(False, "Shift", ValueProperty(shift, -1, device=device, frame_counter=frame_counter))
        self.noso_ratio = NodeSocket(False, "Ratio", ValueProperty(ratio, -1, device=device, frame_counter=frame_counter))

        self.angle_space = None

        super().__init__(device, node_id, frame_counter, "Circles", [
            self.noso_points,
            self.noso_rotation,
            self.noso_frequency,
            self.noso_weights_rad,
            self.noso_scale,
            self.noso_shift,
            self.noso_ratio
        ])

    def initialize(self, width, height, *args):
        super().initialize(width, height)
        if self.noso_weights_rad.get().initial_value is None:
            self.noso_weights_rad.get().initial_value = (
                torch.tensor([1/self.noso_points.get().produce().shape[0]]*self.noso_points.get().produce().shape[0],
                             device=self.device))

        self.angle_space = 2 * torch.pi / self.limit

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
