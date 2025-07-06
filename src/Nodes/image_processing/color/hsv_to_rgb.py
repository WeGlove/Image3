import torch
from src.Nodes.node_socket import NodeSocket
from src.Nodes.node import Node
from src.math.color import hsv_to_rgb


class HSVToRGB(Node):

    def __init__(self, node_id, factory_id):
        self.h = NodeSocket("H")
        self.s = NodeSocket("S")
        self.v = NodeSocket("V")
        super().__init__([self.h, self.s, self.v])

    def produce(self):
        R, G, B = hsv_to_rgb(self.h.get().produce(), self.s.get().produce(), self.v.get().produce())

        out_mask = torch.tensor([R, G, B])

        return out_mask
