from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit


class ByteReader(Node):

    def __init__(self):
        self.initial_value = NodeEdit(".")
        self.reader = None
        super().__init__([], [self.initial_value], "Byte Reader")

    def produce(self):
        return self.reader.read()

    def initialize(self, width, height, excluded_nodes, frame_counter, device):
        super().initialize(width, height, excluded_nodes, frame_counter, device)
        self.reader = open(self.initial_value.get(), "rb")
