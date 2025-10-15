from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.math.gemoetry import dist_line
from src.Nodes.internal.internal_value import InternalValue


class DistLine(Node):

    def __init__(self):
        self.a = NodeSocket("A", default=InternalValue(1.))
        self.b = NodeSocket("B", default=InternalValue(1.))
        self.c = NodeSocket("C", default=InternalValue(1.))
        super().__init__([self.a, self.b, self.c], [], "Returns the given value.")

    def produce(self):
        return dist_line(self.a.get().produce(), self.b.get().produce(), self.c.get().produce(), self.defaults.width,
                         self.defaults.height, self.defaults.device)
