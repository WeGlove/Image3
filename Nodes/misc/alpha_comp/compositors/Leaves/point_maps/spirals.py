from Nodes.misc.alpha_comp.Geos import get_polar
import torch
from Nodes.misc.alpha_comp.compositors.Leaves.point_maps.point_map import PointMap
from Nodes.node_socket import NodeSocket
from Nodes.system.value_property import ValueProperty


class Spirals(PointMap):

    def __init__(self, node_id, device, frame_counter, points=None, rotation=0, frequency=1, weights_angles=None):
        self.noso_points = NodeSocket(False, "Points", ValueProperty(points, -1, device=device, frame_counter=frame_counter))
        self.noso_rotation = NodeSocket(False, "Rotation", ValueProperty(rotation, -1, device=device, frame_counter=frame_counter))
        self.noso_frequency = NodeSocket(False, "Frequency", ValueProperty(frequency, -1, device=device, frame_counter=frame_counter))
        self.noso_weights_angle = NodeSocket(False, "Weights", ValueProperty(weights_angles, -1, device=device, frame_counter=frame_counter))
        self.noso_shift = NodeSocket(False, "Shift", ValueProperty(0, -1, device=device, frame_counter=frame_counter))

        self.angle_space = None
        super().__init__(device, node_id, frame_counter, "Spirals", [
            self.noso_points,
            self.noso_rotation,
            self.noso_frequency,
            self.noso_weights_angle,
            self.noso_shift
        ])

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        if self.noso_weights_angle.get().initial_value is None:
            self.noso_weights_angle.initial_value = torch.tensor([1/self.noso_points.get().produce().shape[0]]*self.noso_points.get().produce().shape[0], device=self.device)

        self.angle_space = 2 * torch.pi / self.limit

    def produce(self):
        rad_out = None
        angles_out = None
        points = self.noso_points.get().produce()
        weights_angle = self.noso_weights_angle.get().produce()
        weights_angle = weights_angle / torch.sum(weights_angle)
        for i in range(points.shape[0]):
            rad, angle = get_polar(self.width, self.height, self.device, points[i])
            angle = angle * weights_angle[i]
            if rad_out is None:
                rad_out = rad
                angles_out = angle
            else:
                rad_out += rad
                angles_out += angle

        angles = (((angles_out + torch.pi) * self.noso_frequency.get().produce() + self.noso_rotation.get().produce()) % (2 * torch.pi)) / (2 * torch.pi)

        arr_map = angles
        arr_map += self.noso_shift.get().produce()

        return arr_map
