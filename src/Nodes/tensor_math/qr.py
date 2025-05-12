from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch


class QR(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.a = NodeSocket(False, "A", default=None, description="")
        super().__init__(node_id, factory_id, "Round", frame_counter, [self.a], device, [])

    def produce(self):
        a = self.a.get().produce()
        Q, R = torch.linalg.qr(a)

        return Q, R

    @staticmethod
    def get_node_name():
        return "QR"
