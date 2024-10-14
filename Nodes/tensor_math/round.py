from Nodes.node import Node
from Nodes.node_socket import NodeSocket
import torch


class Round(Node):

    def __init__(self, node_id, factory_id, device, frame_counter, initial_value="."):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.k = NodeSocket(False, "Bin Size", default=None, description="")
        self.shift = NodeSocket(False, "Shift", default=None, description="")
        super().__init__(node_id, factory_id, "Round", frame_counter, [self.a, self.k, self.shift], device, [])

    def produce(self):
        a = self.a.get().produce()
        k = self.k.get().produce()
        shift = self.shift.get().produce()

        if torch.is_complex(a):
            a.imag = torch.floor(a.imag / k + shift) * k
            a.real = torch.floor(a.real / k + shift) * k
        else:
            a = torch.floor(a / k + shift) * k

        return a

    @staticmethod
    def get_node_name():
        return "Round"
