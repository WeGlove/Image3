from abc import abstractmethod
from Nodes.Node import Node


class PointMap(Node):

    def __init__(self, device, node_id, node_name="PointMap", subnodes=None):
        super().__init__(node_id, node_name, [] if subnodes is None else subnodes, device=device)
        self.device = None
        self.limit = None
        self.width = None
        self.height = None

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
