from Nodes.node import Node


class Compositor(Node):

    def __init__(self, device, node_id, frame_counter, subnode_sockets=None, description="A Compositor Node"):
        super().__init__(node_id, description, frame_counter, [] if subnode_sockets is None else subnode_sockets, device, [])
        self.width = None
        self.height = None
        self.limit = None

    def initialize(self, width, height, limit):
        super().initialize(width, height, limit)
        self.width = width
        self.height = height
        self.limit = limit

    def free(self):
        pass
