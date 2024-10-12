from Nodes.maps.utils.Geos import get_centered_vector_map
from Nodes.maps.point_map import PointMap


class Positions(PointMap):

    def __init__(self, node_id, device, factory_id, frame_counter):
        super().__init__(device, node_id, frame_counter, factory_id, [])

    def produce(self):
        vectors = get_centered_vector_map(self.width, self.height, self.device)
        return vectors

    @staticmethod
    def get_node_name():
        return "Positions"
