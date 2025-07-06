from src.math.Geos import get_polar
import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Spirals(Node):

    def __init__(self):
        self.noso_points = NodeSocket("Points")
        self.noso_rotation = NodeSocket("Rotation")
        self.noso_frequency = NodeSocket("Frequency")
        self.noso_weights_angle = NodeSocket("Weights")
        self.noso_shift = NodeSocket("Shift")

        self.angle_space = None
        super().__init__([self.noso_points, self.noso_rotation, self.noso_frequency, self.noso_weights_angle,
                          self.noso_shift])

    def produce(self):
        rad_out = None
        angles_out = None
        points = self.noso_points.get().produce()
        weights_angle = self.noso_weights_angle.get().produce()
        weights_angle = weights_angle / torch.sum(weights_angle)
        for i in range(points.shape[0]):
            rad, angle = get_polar(self.defaults.width, self.defaults.height, self.defaults.device, points[i])
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
