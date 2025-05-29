from src.Nodes.node import Node
from src.Nodes.interactables.node_edit import NodeEdit
from src.Nodes.node_socket import NodeSocket


class ListGet(Node):

    def __init__(self):
        self.initial_value = NodeEdit("")
        self.compositor = NodeSocket("Compositor")
        super().__init__([self.compositor], [self.initial_value], "Returns the given value.")

    def produce(self):
        text = self.initial_value.get()
        compositor = self.compositor.get().produce()

        return compositor[int(text)]
