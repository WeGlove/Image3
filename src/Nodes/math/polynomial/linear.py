from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.Nodes.internal.internal_value import InternalValue


class Linear(Node):

    def __init__(self):
        self.a = NodeSocket("a", default=InternalValue(1))
        self.b = NodeSocket("b", default=InternalValue(0))
        self.X = NodeSocket("X")
        super().__init__([self.a, self.b, self.X], [], "Keyboard Reader")

    def produce(self):
        return self.a.get().produce() * self.X.get().produce() + self.b.get().produce()
