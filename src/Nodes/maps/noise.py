import torch
from src.Nodes.maps.point_map import PointMap
from src.Nodes.node_socket import NodeSocket


class Noise(PointMap):
    def __init__(self, node_id, factory_id):
        self.bias = NodeSocket(False, "Bias", default=None, description="")
        super().__init__(node_id, factory_id, [self.bias])

    def produce(self):
        noise_map = torch.rand(self.width, self.height, device=self.device) ** self.bias.get().produce()
        return noise_map

    @staticmethod
    def get_node_name():
        return "Noise"
