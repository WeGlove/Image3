from Nodes.node import Node


class PointMap(Node):

    def __init__(self, device, node_id, frame_counter, factory_id, subnodes=None):
        super().__init__(node_id, factory_id, "", frame_counter, [] if subnodes is None else subnodes, device, [])
        self.limit = None
        self.width = None
        self.height = None

    def initialize(self, width, height, limit):
        self.limit = limit
        self.width = width
        self.height = height
        super().initialize(width, height, limit)
