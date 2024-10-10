from Nodes.node import Node
from Nodes.node_socket import NodeSocket


class Addition(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.b = NodeSocket(False, "A", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Keyboard Reader", frame_counter, [self.a, self.b], device, [])

    def produce(self):
        return self.a.get().produce() + self.b.get().produce()

    @staticmethod
    def get_node_name():
        return "Addition"
