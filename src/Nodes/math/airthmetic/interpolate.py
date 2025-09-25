from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.Nodes.system.internal_value import InternalValue


class Interpolate(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.b = NodeSocket("B")
        self.x = NodeSocket("x", default=InternalValue(0))
        self.reader = None
        super().__init__([self.a, self.b, self.x], [], "Interpolate")

    def produce(self):
        return self.a.get().produce() * (1-self.x.get().produce()) + self.b.get().produce() * self.x.get().produce()
