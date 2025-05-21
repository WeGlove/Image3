import torch
from src.Nodes.node import Node
from src.Nodes.node_socket import NodeSocket


class Coloring(Node):

    def __init__(self, node_id, factory_id, device):
        self.device = device
        self.noso_compositor_a = NodeSocket(False, "Compositor A", None)
        self.noso_compositor_b = NodeSocket(False, "Compositor B", None)
        self.noso_compositor_c = NodeSocket(False, "Compositor C", None)
        self.images = []
        super().__init__(node_id, factory_id, "Coloring", [self.noso_compositor_a, self.noso_compositor_b, self.noso_compositor_c], device, [])

    def produce(self):
        mask = torch.stack([self.noso_compositor_a.get().produce(), self.noso_compositor_b.get().produce(),
                            self.noso_compositor_c.get().produce()]).transpose(0, 2) % 1
        return mask * 255

    @staticmethod
    def get_node_name():
        return "Coloring"
