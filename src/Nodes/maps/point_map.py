from src.Nodes.node import Node


class PointMap(Node):

    def __init__(self, device, node_id, frame_counter, factory_id, subnodes=None):
        super().__init__(node_id, factory_id, "", frame_counter, [] if subnodes is None else subnodes, device, [])
        self.width = None
        self.height = None

    def initialize(self, width, height, excluded_nodes, *args):
        super().initialize(width, height, excluded_nodes, *args)
        self.width = width
        self.height = height
