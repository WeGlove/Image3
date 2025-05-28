from src.Nodes.maps.utils.Geos import get_centered_vector_map
from src.Nodes.node import Node


class Positions(Node):

    def produce(self):
        vectors = get_centered_vector_map(self.width, self.height, self.device)
        return vectors
