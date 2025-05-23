import torch
from src.Nodes.maps.point_map import PointMap
from src.Nodes.node_socket import NodeSocket


class iRFFT(PointMap):

    def __init__(self, node_id, factory_id):
        self.input = NodeSocket(False, "Map", None)
        super().__init__(node_id, factory_id, [self.input])

    def produce(self):
        fft = self.input.get().produce()
        mask = torch.fft.irfft2(fft)

        return mask

    @staticmethod
    def get_node_name():
        return "iRFFT"
