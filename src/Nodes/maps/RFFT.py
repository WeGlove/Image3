import torch
from src.Nodes.maps.point_map import PointMap
from src.Nodes.node_socket import NodeSocket


class RFFT(PointMap):

    def __init__(self, node_id, device, factory_id):
        self.input = NodeSocket(False, "Map", None)
        super().__init__(device, node_id, factory_id, [self.input])

    def produce(self):
        mask = self.input.get().produce()
        fft = torch.fft.rfft2(mask)

        return fft

    @staticmethod
    def get_node_name():
        return "RFFT"
