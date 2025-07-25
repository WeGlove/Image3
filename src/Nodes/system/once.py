from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Once(Node):

    def __init__(self):
        self.input = NodeSocket("Input")
        self.last = None
        self.last_frame = -1
        super().__init__([self.input], [], "Returns the first produced value")

    def produce(self):
        if self.last_frame == self.frame_counter.get():
            return self.last

        self.last_frame = self.frame_counter.get()
        self.last = self.input.get().produce()
        return self.last

    def initialize(self, defaults, excluded_nodes, frame_counter):
        super().initialize(defaults, excluded_nodes, frame_counter)
        self.last_frame = -1
        self.last = None
