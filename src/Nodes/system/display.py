from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit
from src.Nodes.node_socket import NodeSocket


class Display(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.initial_value = NodeEdit("")
        super().__init__([self.a], [self.initial_value], "Returns the given value.")

    def produce(self):
        a = self.a.get().produce()
        self.initial_value.set(a)

        return a
