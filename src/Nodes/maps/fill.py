import torch
from src.Nodes.maps.point_map import PointMap
from src.Nodes.node_socket import NodeSocket


class Fill(PointMap):

    def __init__(self, node_id, factory_id):
        self.input_noso = NodeSocket(False, "Input", None)
        super().__init__(node_id, factory_id, [self.input_noso])

    def produce(self):
        return torch.ones((self.width, self.height), device=self.device) * self.input_noso.get().produce()

    @staticmethod
    def get_node_name():
        return "Fill"
