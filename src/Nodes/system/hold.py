from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Hold(Node):

    def __init__(self):
        self.input = NodeSocket(False, "Input", default=None, description="")
        self.start = NodeSocket(False, "Start", default=None, description="")
        self.last = None
        self.last_frame = -1
        super().__init__([self.input, self.start], [], "Returns the given value.")

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

    def initialize(self, defaults, excluded_nodes, frame_counter):
        super().initialize(defaults, excluded_nodes, frame_counter)
        self.last_frame = -1
        self.last = None
