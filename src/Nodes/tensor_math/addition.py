from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Addition(Node):

    def __init__(self, node_id, factory_id):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.b = NodeSocket(False, "A", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Keyboard Reader", [self.a, self.b], [])

    def produce(self):
        return self.a.get().produce() + self.b.get().produce()

    @staticmethod
    def get_node_name():
        return "Addition"
