from src.Nodes.node import Node
from src.interactables.node_edit import NodeEdit


class ByteReader(Node):

    def __init__(self):
        self.initial_value = NodeEdit(".")
        self.reader = None
        super().__init__([], [self.initial_value], "Byte Reader")

    def produce(self):
        return self.reader.read()

    def initialize(self, defaults, excluded_nodes, frame_counter):
        super().initialize(defaults, excluded_nodes, frame_counter)
        self.reader = open(self.initial_value.get(), "rb")
