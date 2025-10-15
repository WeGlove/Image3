from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.Nodes.internal.internal_value import InternalValue


class Division(Node):

    def __init__(self):
        self.a = NodeSocket("A", default=InternalValue(1))
        self.b = NodeSocket("B", default=InternalValue(1))
        self.reader = None
        super().__init__([self.a, self.b], [], "Division")

    def produce(self):
        return self.a.get().produce() / self.b.get().produce()
