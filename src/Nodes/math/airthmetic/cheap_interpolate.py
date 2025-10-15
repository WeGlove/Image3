from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.Nodes.internal.internal_value import InternalValue


class CheapInterpolate(Node):

    def __init__(self):
        self.a = NodeSocket("A")
        self.b = NodeSocket("B")
        self.x = NodeSocket("x", default=InternalValue(0))
        self.reader = None
        super().__init__([self.a, self.b, self.x], [], "Interpolate")

    def produce(self):
        x = self.x.get().produce()
        if x == 0:
            return self.a.get().produce()
        elif x == 1:
            return self.b.get().produce()
        return self.a.get().produce() * (1-x) + self.b.get().produce() * x
