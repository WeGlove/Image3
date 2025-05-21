from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Hold(Node):

    def __init__(self, node_id, factory_id):
        self.input = NodeSocket(False, "Input", default=None, description="")
        self.start = NodeSocket(False, "Start", default=None, description="")
        self.last = None
        self.last_frame = -1
        super().__init__(node_id, factory_id, "Returns the given value.",
                         [self.input, self.start], [])

    def produce(self):
        if self.last is None:
            self.last_frame = self.frame_counter.get()
            self.last = self.start.get().produce()
            return self.last

        if self.last_frame == self.frame_counter.get():
            return self.last

        self.last_frame = self.frame_counter.get()
        out = self.last
        self.last = self.input.get().produce()
        return out

    def initialize(self, width, height, excluded_nodes, frame_counter, device):
        super().initialize(width, height, excluded_nodes, frame_counter, device)
        self.last_frame = -1
        self.last = None

    @staticmethod
    def get_node_name():
        return "Hold"
