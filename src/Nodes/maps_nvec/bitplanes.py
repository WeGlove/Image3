import torch
from src.Nodes.node_socket import NodeSocket
from src.Nodes.maps.point_map import PointMap


class BitPlanes(PointMap):

    def __init__(self, node_id, factory_id, device, frame_counter):
        self.input = NodeSocket(False, "Input", default=None, description="")
        super().__init__(device, node_id, frame_counter, factory_id, [self.input])

    def produce(self):
        mask = self.input.get().produce()
        mask = torch.tensor(mask, dtype=torch.int8)

        bitplanes = []
        for i in range(8):
            bitplane = mask % 2
            mask = mask >> 1
            bitplanes.append(bitplane)

        return torch.tensor(bitplanes, device=self.device)

    @staticmethod
    def get_node_name():
        return "BitPlanes"
