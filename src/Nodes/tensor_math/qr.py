from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch


class QR(Node):

    def __init__(self):
        self.a = NodeSocket(False, "A", default=None, description="")
        super().__init__([self.a], [], "Round")

    def produce(self):
        a = self.a.get().produce()
        Q, R = torch.linalg.qr(a)

        return Q, R
