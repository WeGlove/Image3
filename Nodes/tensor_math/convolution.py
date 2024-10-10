from Nodes.node import Node
from Nodes.node_socket import NodeSocket
import torch
from scipy.signal import fftconvolve
from torch.nn.functional import conv2d


class Convolution(Node):

    def __init__(self, node_id, factory_id, device, frame_counter):
        self.a = NodeSocket(False, "A", default=None, description="")
        self.b = NodeSocket(False, "B", default=None, description="")
        self.reader = None
        super().__init__(node_id, factory_id, "Convolution", frame_counter, [self.a, self.b], device, [])

    def produce(self):
        #mask = fftconvolve(self.a.get().produce().cpu(), self.b.get().produce().cpu())
        a = self.a.get().produce()
        a = torch.reshape(a, (1, 1, *a.shape))
        b = self.b.get().produce()
        b = torch.reshape(b, (1, 1, *b.shape))
        mask = conv2d(a, b, padding="same")
        mask = mask[0][0]
        print(mask.shape)
        return mask

    @staticmethod
    def get_node_name():
        return "Convolution"
