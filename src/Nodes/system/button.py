from src.Nodes.node import Node
from src.interactables.node_button import NodeButton


class Button(Node):

    def __init__(self):
        self.initial_value = NodeButton(None)
        super().__init__([], [self.initial_value], "Returns the given value.")

    def produce(self):
        text = self.initial_value.get()
        return text
