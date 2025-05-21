from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Once(Node):

    def __init__(self, node_id, factory_id):
        self.input = NodeSocket(False, "Input", default=None, description="")
        self.last = None
        self.last_frame = -1
        super().__init__(node_id, factory_id, "Returns the given value.", [self.input], [])

    def produce(self):
        if self.last_frame == self.frame_counter.get():
            return self.last

        self.last_frame = self.frame_counter.get()
        self.last = self.input.get().produce()
        return self.last

    def initialize(self, width, height, excluded_nodes, frame_counter, device):
        super().initialize(width, height, excluded_nodes, frame_counter, device)
        self.last_frame = -1
        self.last = None

    @staticmethod
    def get_node_name():
        return "Once"
