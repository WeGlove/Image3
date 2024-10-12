from Nodes.maps.utils.Geos import get_centered_vector_map
import torch
from Nodes.maps.point_map import PointMap
from Nodes.node_socket import NodeSocket


class Fill(PointMap):

    def __init__(self, node_id, device, factory_id, frame_counter):
        self.input_noso = NodeSocket(False, "Input", None)
        super().__init__(device, node_id, frame_counter, factory_id, [self.input_noso])

    def produce(self):
        return torch.ones((self.width, self.height)) * self.input_noso.get().produce()

    @staticmethod
    def get_node_name():
        return "Fill"
