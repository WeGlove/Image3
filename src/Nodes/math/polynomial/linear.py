from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Linear(Node):

    def __init__(self):
        self.a = NodeSocket("a")
        self.b = NodeSocket("b")
        self.X = NodeSocket("X")
        self.reader = None
        super().__init__([self.a, self.b, self.X], [], "Keyboard Reader")

    def produce(self):
        return self.a.get().produce() * self.X.get().produce() + self.b.get().produce()
