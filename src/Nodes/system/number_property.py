from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit


class NumberProperty(Node):

    def __init__(self):
        self.initial_value = NodeEdit(0)
        super().__init__([], [self.initial_value], "Returns the given value.")

    def produce(self):
        text = self.initial_value.get()
        return float(text)
