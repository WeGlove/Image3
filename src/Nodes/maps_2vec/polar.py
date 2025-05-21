from src.Nodes.maps.utils.Geos import get_polar
import torch
from src.Nodes.maps.point_map import PointMap
from src.Nodes.node_socket import NodeSocket


class Polar(PointMap):

    def __init__(self, node_id, factory_id):
        self.center = NodeSocket(False, "Center", None)
        self.angle_shift = NodeSocket(False, "Angle Shit", None)
        super().__init__(node_id, factory_id, [self.center, self.angle_shift])

    def produce(self):
        radius, angle = get_polar(self.width, self.height, self.device, self.center.get().produce())
        angle = (angle / torch.pi + 1) / 2
        angle += self.angle_shift.get().produce()
        angle %= 1

        return torch.stack([radius, angle])

    @staticmethod
    def get_node_name():
        return "Polar"
