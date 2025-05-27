import torch
from src.Nodes.maps.point_map import PointMap
from src.Nodes.node_socket import NodeSocket
from src.Nodes.system.number_property import NumberProperty


class Fill(PointMap):

    def __init__(self, node_id, factory_id):
        self.input_noso = NodeSocket(False, "Input", NumberProperty(-1, "None"))
        super().__init__(node_id, factory_id, [self.input_noso])

    def produce(self):
        return torch.ones((self.height, self.width), device=self.device) * self.input_noso.get().produce()

    @staticmethod
    def get_node_name():
        return "Fill"
