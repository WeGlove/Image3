from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Transposition(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.dim_1 = NodeSocket(False, "Dim 1", default=None, description="")
        self.dim_2 = NodeSocket(False, "Dim 2", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Division", frame_counter,
                         [self.a, self.dim_1, self.dim_2], device, [])

    def produce(self):
        return self.a.get().produce().transpose(self.dim_1.get().produce(), self.dim_2.get().produce())

    @staticmethod
    def get_node_name():
        return "Transposition"
