from Nodes.node import Node
from Nodes.node_socket import NodeSocket
import torch


class SVD(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.a = NodeSocket(False, "A", default=None, description="")
        super().__init__(node_id, factory_id, "Round", frame_counter, [self.a], device, [])

    def produce(self):
        a = self.a.get().produce()
        U, S, Vh = torch.linalg.svd(a)
        S = torch.diag(S, diagonal=U.shape[0] - Vh.shape[0])
        S = S[:, -Vh.shape[0]:]
        a = S.cpu().numpy()
        print(float(S[0, 0]), float(S[1,1]))

        print(U.shape, S.shape, Vh.shape)

        return U, S, Vh

    @staticmethod
    def get_node_name():
        return "SVD"
