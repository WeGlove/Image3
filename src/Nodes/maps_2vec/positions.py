from src.Nodes.maps.utils.Geos import get_centered_vector_map
from src.Nodes.maps.point_map import PointMap


class Positions(PointMap):

    def __init__(self, node_id, factory_id):
        super().__init__(node_id, factory_id, [])

    def produce(self):
        vectors = get_centered_vector_map(self.width, self.height, self.device)
        return vectors

    @staticmethod
    def get_node_name():
        return "Positions"
