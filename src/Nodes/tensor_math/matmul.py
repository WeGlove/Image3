from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch


class Matmul(Node):

    def __init__(self, node_id, factory_id, device, initial_value="."):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.b = NodeSocket(False, "B", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Matmul", [self.a, self.b], device, [])

    def produce(self):
        return torch.matmul(self.a.get().produce(), self.b.get().produce())

    @staticmethod
    def get_node_name():
        return "Matmul"
