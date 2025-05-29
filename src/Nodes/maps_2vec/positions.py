from src.Nodes.maps.utils.Geos import get_centered_vector_map
from src.Nodes.node import Node


class Positions(Node):

    def produce(self):
        vectors = get_centered_vector_map(self.defaults.width, self.defaults.height, self.defaults.device)
        return vectors
