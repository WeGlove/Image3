from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
from src.math.gemoetry import dist_line


class DistGeometryLine(Node):

    def __init__(self):
        self.a = NodeSocket("A", None)
        self.b = NodeSocket("B", None)
        self.c = NodeSocket("C", None)
        super().__init__([self.a, self.b, self.c], [], "Returns the given value.")

    def produce(self):
        return dist_line(self.a.get().produce(), self.b.get().produce(), self.c.get().produce(), self.defaults.width,
                         self.defaults.height, self.defaults.device)
