from abc import abstractmethod
from alpha_comp.Node import Node


class PointMap(Node):

    def __init__(self, node_name="PointMap", animated_properties=None):
        super().__init__(node_name)
        self.device = None
        self.limit = None
        self.width = None
        self.height = None
        self.set_animate_properties(animated_properties)

    def initialize(self, width, height, limit, device=None):
        self.device = device
        self.limit = limit
        self.width = width
        self.height = height

    @abstractmethod
    def composite(self, index, img):
        pass

    def get_animated_properties(self, visitors):
        pass
