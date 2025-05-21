from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Mean(Node):

    def __init__(self, node_id, factory_id, device, initial_value="."):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.b = NodeSocket(False, "B", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Subtraction", [self.a, self.b], device, [])

    def produce(self):
        return (self.a.get().produce() + self.b.get().produce()) / 2

    @staticmethod
    def get_node_name():
        return "Mean"
