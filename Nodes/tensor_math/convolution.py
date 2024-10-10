from Nodes.node import Node
from Nodes.node_socket import NodeSocket
import torch
from scipy.signal import fftconvolve


class Convolution(Node):

    def __init__(self, node_id, factory_id, device, frame_counter):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.b = NodeSocket(False, "B", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Convolution", frame_counter, [self.a, self.b], device, [])

    def produce(self):
        mask = fftconvolve(self.a.get().produce().cpu(), self.b.get().produce().cpu())
        return torch.tensor(mask, device=self.device)

    @staticmethod
    def get_node_name():
        return "Convolution"
