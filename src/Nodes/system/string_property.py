from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit


class StringProperty(Node):

    def __init__(self):
        self.initial_value = NodeEdit("")
        super().__init__([], [self.initial_value], "Returns the given value.")

    def produce(self):
        text = self.initial_value.get()
        return text
