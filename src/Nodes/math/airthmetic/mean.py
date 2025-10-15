from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.Nodes.internal.internal_value import InternalValue


class Mean(Node):

    def __init__(self):
        self.a = NodeSocket("A", default=InternalValue(1))
        self.b = NodeSocket("B", default=InternalValue(1))
        self.reader = None
        super().__init__([self.a, self.b], [], "Subtraction")

    def produce(self):
        return (self.a.get().produce() + self.b.get().produce()) / 2
