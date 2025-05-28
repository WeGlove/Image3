from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Addition(Node):

    def __init__(self):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.b = NodeSocket(False, "A", default=None, description="")
        self.reader = None
        super().__init__([self.a, self.b], [], "Keyboard Reader")

    def produce(self):
        return self.a.get().produce() + self.b.get().produce()
