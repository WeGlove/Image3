import torch
from src.Nodes.maps.point_map import PointMap
from src.Nodes.node_socket import NodeSocket


class Swap(PointMap):

    def __init__(self, node_id, device, factory_id):
        self.sample = NodeSocket(False, "Sample", None)
        self.map = NodeSocket(False, "Map", None)
        super().__init__(device, node_id, factory_id, [self.map, self.sample])

    def produce(self):
        positions = self.map.get().produce()
        positions = positions[0, ...] * positions[1, ...]
        positions = positions.flatten(0, 1)
        positions = torch.tensor(positions, dtype=torch.int64, device=self.device)
        positions = positions % positions.shape[0]

        sample = self.sample.get().produce()
        sample = torch.flatten(sample, -2, -1)

        sampled = torch.index_select(sample, 0, positions)
        sampled = torch.reshape(sampled, (self.width, self.height))

        return sampled

    @staticmethod
    def get_node_name():
        return "Swap"
