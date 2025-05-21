from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket
import torch


class SVD(Node):

    def __init__(self, node_id, factory_id):
        self.a = NodeSocket(False, "A", default=None, description="")
        super().__init__(node_id, factory_id, "Round", [self.a], [])

    def produce(self):
        a = self.a.get().produce()
        U, S, Vh = torch.linalg.svd(a)
        S = torch.diag(S, diagonal=U.shape[0] - Vh.shape[0])
        S = S[:, -Vh.shape[0]:]

        return U, S, Vh

    @staticmethod
    def get_node_name():
        return "SVD"
