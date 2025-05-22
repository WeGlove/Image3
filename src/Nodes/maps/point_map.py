from src.Nodes.node import Node


class PointMap(Node):

    def __init__(self, node_id, factory_id, subnodes=None):
        super().__init__(node_id, factory_id, "", [] if subnodes is None else subnodes, [])

    def initialize(self, width, height, excluded_nodes, *args):
        super().initialize(width, height, excluded_nodes, *args)
