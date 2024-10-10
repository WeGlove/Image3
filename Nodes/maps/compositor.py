from Nodes.node import Node


class Compositor(Node):

    def __init__(self, device, node_id, factory_id, frame_counter, subnode_sockets=None, description="A Compositor Node"):
        super().__init__(node_id, factory_id, description, frame_counter, [] if subnode_sockets is None else subnode_sockets, device, [])
        self.width = None
        self.height = None

    def initialize(self, width, height, *args):
        super().initialize(width, height, *args)
        self.width = width
        self.height = height

    def free(self):
        pass
