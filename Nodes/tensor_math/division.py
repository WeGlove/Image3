from Nodes.node import Node
from Nodes.node_socket import NodeSocket


class Division(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.b = NodeSocket(False, "B", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Division", frame_counter, [self.a, self.b], device, [])

    def produce(self):
        return self.a.get() / self.b.get()

    @staticmethod
    def get_node_name():
        return "Division"
