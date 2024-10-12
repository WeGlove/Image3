from Nodes.maps.utils.Geos import get_polar
import torch
from Nodes.maps.point_map import PointMap


class Polar(PointMap):

    def __init__(self, node_id, device, factory_id, frame_counter):
        super().__init__(device, node_id, frame_counter, factory_id, [])

    def produce(self):
        radius, angle = get_polar(self.width, self.height, self.device)

        return torch.stack([radius, angle])

    @staticmethod
    def get_node_name():
        return "Polar"
