from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Interpolate(Node):

    def __init__(self, node_id, factory_id):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.b = NodeSocket(False, "B", default=None, description="")
        self.x = NodeSocket(False, "x", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Interpolate", [self.a, self.b, self.x], [])

    def produce(self):
        return self.a.get().produce() * (1-self.x.get().produce()) + self.b.get().produce() * self.x.get().produce()

    @staticmethod
    def get_node_name():
        return "Interpolate"
